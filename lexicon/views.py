from django.shortcuts import render
from django.conf import settings
from models import *
from lib.custom_text import Text 
import nltk
from nltk.corpus import stopwords, names
from db_backend.learner_api_query import add_learner
from db_backend.collegiate_api_query import add_collegiate
from variables.pos import pos_freq_initial, coca_pos_dict, pos_ignore_list
from variables.short import coca_short_4000
import logging
import copy
import math

#////////////////////////////////////////////////////////////
# Lemmatization 
#////////////////////////////////////////////////////////////

def stop_word(token):
    if not token[0].isalpha(): return True
    if '-' in token: return True
    ignored_words = stopwords.words('english')
    return token in ignored_words
        
def _lemma_coca(token):
    cluster = []
    try:
        wp = WordPointer.objects.get(word=token.lower())
    except:
        return cluster        
    for word in wp.coca.all():
        cluster.append(word.lemma)
    return cluster
    
def _lemma_dict(token):
    cluster = []
    try:
        wp = WordPointer.objects.get(word=token.lower())
    except:
        return cluster
    for w in wp.dict_lemmas.all():
        cluster.append(w.headword)
    return cluster
        
def _lemma(token):
    cluster = []
    try:
        wp = WordPointer.objects.get(word=token.lower())
    except:
        return cluster
    for w in wp.lemmas.all():
        cluster.append(w.word)
    return cluster
    
def lemma(tokens):
    if isinstance(tokens, basestring):
        token = tokens.lower()
        cluster = []
        if tokens not in cluster: 
            cluster.extend(_lemma(token))
        if False and tokens not in cluster: 
            cluster.extend(_lemma_coca(token))
        if cluster == [] and new_word(token): 
            return lemma(token)
        cluster = list(set(cluster))
        return cluster

    if isinstance(tokens, dict):
        dictlist=[]
        for key, value in tokens.iteritems():
            dictlist.append(key)
        return lemma(dictlist)    
        
    cluster = []
    for i,token in enumerate(tokens):
        #print cluster
        #print token
        print i
        flag = True
        if stop_word(token):
            cl = []
        else:
            cl = lemma(token)
            #for c in cl:
            #    cl = cl+ lemma(c)
        #print cluster
        for l in cl:
            for n,c in enumerate(cluster):
                #print c
                if l in c['lemmas']:
                    flag = False
                    #cluster[n]['lemmas'] = list(set(cl+cluster[n]['lemmas']))
                    c['lemmas'] = list(set(cl+c['lemmas']))
                    c['tokens'].append(token)
        if flag and cl!=[]: cluster.append({'tokens':[token],'lemmas':cl})
    return cluster
                    
#////////////////////////////////////////////////////////////
# Update New Word 
#////////////////////////////////////////////////////////////

def new_word(token, force_add = False):
    if any(char.isdigit() for char in token): return False
    undef,created = UndefinedWordPointer.objects.get_or_create(word=token)
    if (not settings.UNDEFINED_UPDATE and not force_add) or undef.undefined: return False
    added = False
    added = add_learner(token) or added
    added = add_collegiate(token) or added
    if added and WordPointer.objects.filter(word=token).count()>0 and WordPointer.objects.get(word=token).entry_number !=0:
        undef.delete()
        return True
    else:
        undef.undefined = True
        undef.save()
        return False

#////////////////////////////////////////////////////////////
# Glossary Data Generator
#////////////////////////////////////////////////////////////
        
class Glossary(object):
    def __init__(self, tokens, text=Text(''), gid=0, concordance=[], pos_dict={},cutoff = 1000):
        #major properies
        self.gid = str(gid)
        self.freq = 0.0
        self.difficulty = 0.0
                
        self.entry_list = []

        #searching support properties
        self.pos_freq = []
        self.pos_type_dict = {}
        self.concordance = concordance
        #intermediate properties
        self.pos_list = []
        self.lemmas = []
        self.tokens = tokens['tokens']
        self.tokens_pos = []
        n = -1
        
        
        for token in self.tokens:
            self.concordance = self.concordance + text.concordance(token)
            if token in pos_dict.keys():
                self.tokens_pos = self.tokens_pos + pos_dict[token]
        
        for token in tokens['lemmas']:
            if token in coca_short_4000[:cutoff]:
                self.entry_dict = {}
                return
            self._add_pos_freq(token)

            flag =  True
            for n,ep in enumerate(WordPointer.objects.get(word=token).entry()):
                if ep.has_def: self._add_entry(ep)
                flag = False

            if flag: 
                new_word(token)
            else:
                self.lemmas.append(token)
            
        
        
        self._calc_difficulty()
        self.pos_list = list(set(self.pos_list))
        self.tokens_pos = list(set(self.tokens_pos))
        
            
    def _add_pos_freq(self,token):
        pos_freq = copy.deepcopy(pos_freq_initial)
        #print token
        coca_exist = False
        for coca in WordPointer.objects.get(word=token).coca_as_lemma.all():
            coca_exist = True
            self.freq = self.freq + coca.freq(typ='coca') 
            if coca.pos in coca_pos_dict:
                pos_freq[coca_pos_dict[coca.pos]] += coca.freq(typ='coca') 
            #print pos_freq 
        for pos, freq in pos_freq.iteritems():
            if freq != 0:
                self.pos_freq.append({'headword':token, 'pos':pos, 'freq':freq})
        if not coca_exist:  
            ngrams = Ngrams.objects.filter(word = token)
            if ngrams.count()>0: self.freq = self.freq + float(ngrams[0].raw_freq)
        return 
        
    def _add_entry(self, ep):
        #if [ep.__class__.__name__, ep.entry_id] in self.entry_info: return
        entry_id =  ep.entry_id
        self.entry_list.append(entry_id)
        t = ep.headword+','+ep.dict_type+','+ep.pos
        if t not in self.pos_type_dict: self.pos_type_dict[t]=entry_id
        self.pos_list.append(ep.pos)
        
    def _calc_difficulty(self):
        easybase=6e2
        diffbase=1e-1
        factor=10/math.log(diffbase/easybase,10)
        freq = self.freq if self.freq != 0.0 else 32.0/464
        #self.difficulty = - math.log(freq/10000000000,10)   
        self.difficulty = math.log(float(freq)/easybase,10)*factor
    def serialize(self):
        return self.__dict__
         
def glossary_filter(g):
    if g.entry_list == []: return False
    if g.freq == 0 and ( len(g.lemmas[0])<4 or 
        (g.pos_list==['noun'] and g.lemmas[0] in names.words())): 
        return False
    for pos in pos_ignore_list:
        if pos in g.pos_list: return False
    for pos in g.tokens_pos:
        if 'NNP' in pos: return False
    return True

def glossary_wrapper(tokens_list, text,pos_dict={}):
    glossary_dict = {}
    for n, tokens in enumerate(tokens_list):
            g = Glossary(tokens,text,gid=n, pos_dict=pos_dict)
            if glossary_filter(g):                
                glossary_dict[str(n)]=g.serialize()
            print n
    return glossary_dict   
 
#////////////////////////////////////////////////////////////
# Text Analyze 
#////////////////////////////////////////////////////////////

def analyze(text):
    punctuation = { 0x2018:0x27, 0x2019:0x27, 0x201C:0x22, 0x201D:0x22,}
#                    0x5be:0x2d,0x1806:0x2d,0x2010:0x2d,0x2011:0x2d,0x2012:0x2d,
#                    0x2013:0x2d,0x2014:0x2d,0x2015:0x2d,
#                    0x2212:0x2d,0xfe58:0x2d,0xfe63:0x2d,0xff0d:0x2d,}
    try:
     text = text.translate(punctuation)
     text = text.replace('\'',' \' ').replace('"',' " ')
     text = text.replace(u'\u2014',u' \u2014 ')
     tokens = nltk.word_tokenize(text)
    except:
     text=text.decode('utf-8')
     text = text.translate(punctuation)
     text = text.replace('\'',' \' ').replace('"',' " ')
     text = text.replace(u'\u2014',u' \u2014 ')
     tokens = nltk.word_tokenize(text)    
    pos_tag = nltk.pos_tag(tokens)
    pos_dict = {}
    for pos in pos_tag:
        if pos[0] not in pos_dict.keys(): pos_dict[pos[0]] = []
        pos_dict[pos[0]] = pos_dict[pos[0]] + [pos[1]]
    text = Text(tokens)
    vocab = text.vocab()
    tokens_list = lemma(vocab)
    glossary_dict = glossary_wrapper(tokens_list,text,pos_dict)
    return glossary_dict, tokens
    