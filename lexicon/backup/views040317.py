from django.shortcuts import render
from django.conf import settings
from models import *
from nltk.text import Text 
import nltk
from nltk.corpus import stopwords, names
from db_backend.learner_api_query import add_learner
from db_backend.collegiate_api_query import add_collegiate
from variables.pos import pos_freq_initial, coca_pos_dict, pos_ignore_list
from variables.short import coca_short_4000
import logging
import copy

#////////////////////////////////////////////////////////////
# Lemmatization 
#////////////////////////////////////////////////////////////

def stop_word(token):
    if not token[0].isalpha(): return True
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
    
def _lemma_learner(token):
    cluster = []
    try:
        wp = WordPointer.objects.get(word=token.lower())
    except:
        return cluster
    for w in wp.learner_lemmas.all():
        cluster.append(w.headword)
    return cluster
    
def _lemma_collegiate(token):
    cluster = []
    try:
        wp = WordPointer.objects.get(word=token.lower())
    except:
        return cluster
    for w in wp.collegiate_lemmas.all():
        cluster.append(w.headword)
    return cluster    
    
def lemma(tokens):
    if isinstance(tokens, basestring):
        token = tokens.lower()
        cluster = []
        if tokens not in cluster: 
            cluster.extend(_lemma_learner(token))
        if tokens not in cluster: 
            cluster.extend(_lemma_collegiate(token))
        if True and tokens not in cluster: 
            cluster.extend(_lemma_coca(token))
        if cluster == [] and new_word(token): 
            return lemma(token)
        cluster = list(set(cluster))
        #print token
        #print cluster
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
        for l in cl:
            for n,c in enumerate(cluster):
                if l in c:
                    flag = False
                    cluster[n] = list(set(cl+cluster[n]))
        if flag and cl!=[]: cluster.append(cl)
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

def undefined_update():
    #print LearnerRaw.objects.filter(alpha = 'addition')
    #add_learner('addition')
    #return
    for n, undef in enumerate(UndefinedWordPointer.unprocessed()):
        token = undef.word
        added = False
        added = add_learner(token) or added
        added = add_collegiate(token) or added
        print n, token
        if added and WordPointer.objects.filter(word=token).count()>0 and WordPointer.objects.get(word=token).entry_number !=0:
            undef.delete()
        else:
            undef.undefined = True
            undef.save()

#////////////////////////////////////////////////////////////
# Glossary Data Generator
#////////////////////////////////////////////////////////////

class GlossaryEntry(object):
    def __init__(self, ep, eid):
        self.headword = ep.headword
        self.type = ep.__class__.__name__
        self.data = ep.data
        self.eid = eid
        self.pos = ep.pos
        self.entry_id = ep.entry_id
    def __unicode__(self):
        return self.headword
        
class Glossary(object):
    def __init__(self, tokens, gid=0, cutoff = 1000):
        self.gid = gid
        self.pos_freq = {}
        self.pos_list = []
        self.entry_dict = {}
        self.entry_info = []
        self.pos_type_dict = {}
        self.freq = 0
        self.difficulty = 0
        eid = 0
        n = -1
        #print tokens
        for token in tokens:
            if token in coca_short_4000[:cutoff]:
                self.entry_dict = {}
                return
            self._add_pos_freq(token)
            #print token
            flag =  True
            for n,ep in enumerate(WordPointer.objects.get(word=token).entry('learner')):
                #print eid, n, eid+n+1
                self._add_entry(ep, eid+n)
                flag = False
            #if flag: 
            #    print token
            #    new_word(token)
            eid = n+1    
            if False or len(self.entry_dict) == 0:
                flag =  True
                for n,ep in enumerate(WordPointer.objects.get(word=token).entry('collegiate')):
                    self._add_entry(ep, eid+n)
                    flag = False
                if flag: 
                    #print token
                    new_word(token)
        self._calc_difficulty()
        self.pos_list = list(set(self.pos_list))

            
    def _add_pos_freq(self,token):
        pos_freq = copy.deepcopy(pos_freq_initial)
        #print token
        for coca in WordPointer.objects.get(word=token).coca_as_lemma.all():
            #print coca
            #print coca.pos, coca.raw_freq
            self.freq = self.freq + coca.raw_freq
            #print 'freq', self.freq 
            if coca.pos in coca_pos_dict:
                pos_freq[coca_pos_dict[coca.pos]] += coca.raw_freq 
            #print pos_freq 
        self.pos_freq[token] = pos_freq
        return 
        
    def _add_entry(self, ep, eid):
        #if [ep.__class__.__name__, ep.entry_id] in self.entry_info: return
        self.entry_info.append([ep.__class__.__name__, ep.entry_id])
        self.entry_dict[eid]=GlossaryEntry(ep,eid)
        self.pos_type_dict[ep.headword+','+ep.__class__.__name__+','+ep.pos]=eid
        self.pos_list.append(self.entry_dict[eid].pos)
    def _calc_difficulty(self):
         self.difficulty = self.freq   

def glossay_wrapper(tokens_list):
    cluster = []
    for n, tokens in enumerate(tokens_list):
            g = Glossary(tokens,gid=n)
            if glossary_filter(g):                
                cluster.append(Glossary(tokens,gid=n))
            print n
    return cluster   
          
def glossary_filter(g):
    if g.entry_dict == {}: return False
    if g.freq == 0 and ( len(g.entry_dict[0].headword)<4 or 
        (g.pos_list==['noun'] and g.entry_dict[0].headword.title() in names.words())): 
        return False
    for pos in pos_ignore_list:
        if pos in g.pos_list: return False
    return True

#////////////////////////////////////////////////////////////
# Text Analyze 
#////////////////////////////////////////////////////////////

def analyze(text):
    text=text.decode('utf-8')
    tokens = nltk.word_tokenize(text)
    vocab = Text(tokens).vocab()
    tokens_list = lemma(vocab)
    glossary = glossay_wrapper(tokens_list)
    return glossary
    