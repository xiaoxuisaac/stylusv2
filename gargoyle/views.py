#from __future__ import print_function
import os as _os
import warnings as _warnings
import datetime
import string
import json
import pickle
import copy
from subprocess import Popen, PIPE
import subprocess
from tempfile import mkdtemp
from random import shuffle
import random
import zipfile

from django.shortcuts import render
from django.forms import formset_factory
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template.loader import get_template
from django.core.files.uploadedfile import SimpleUploadedFile

from lexicon.views import analyze
from ocr.models import OcrFile
from .models import *
from .forms import *
from .signals import *

#////////////////////////////////////////////////////////////
# Protal  
#////////////////////////////////////////////////////////////

def homepage(request):
    passage_form =PassageForm()
    #logger.info(get_ip(request)+' Visiting Home Page')
    file_form = FilesForm()
    return render(request,'homepage.html',{'passage_form':passage_form,'csv_form':file_form})


def feedback(request):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.save()
        return render(request,'comment_success.html')
    else:
        return render(request,'comment.html',{'comment_form':CommentForm()})


def vocab(request,prepare='n'):
    if request.method == 'POST':# and '_text' in request.POST:
        form = PassageForm(request.POST)
        if form.is_valid():
            #////Constructing Name Form//////////////
            name='Untitled' if form.cleaned_data['name'] ==  '' else form.cleaned_data['name']
            if form.cleaned_data['request_id'] ==  '' or prepare == 'pid':             
                request_id = '|'.join([request.user.get_username(),datetime.date.today().isoformat(),name,id_generator()])
            else:
                request_id = form.cleaned_data['request_id']
            name_form = NameForm(initial={'name':name,'project':'Homer Project','request_id':request_id},prefix='name')


            session_var, created = SessionVariables.objects.get_or_create(request_id=request_id)
            #////If preparing request_id//////////////
            if prepare == 'pid':
                return HttpResponse(request_id)
            
            #////If retrieving data by request_id//////////////
            if session_var.glossary_dict != None and prepare != 'prepare':
                update_session(request, session_var)
                glossary_dict = request.session['glossary_dict']
                select_table = request.session['select_table']

                vocab_formset = initialize_vocab_formset(select_table, glossary_dict)
                session_var.initial_select_table = pickle.dumps(select_table)
                session_var.save()
                update_session(request, session_var)
                return render(request,'vocabs.html',{'formset':vocab_formset,'name_form':name_form,'title':'Vocabulary in'})            
            
            #////Constructing Vocab Form/////////////                
            content = form.cleaned_data['content']
            glossary_dict, tokens = analyze(content, session_var=session_var)
            select_table = vocab_select(glossary_dict, request=request)
            
            #////Storing Session Variables///////////
            #session_var.select_table = pickle.dumps(select_table)
            session_var.initial_select_table = pickle.dumps(select_table)
            session_var.glossary_dict = pickle.dumps(glossary_dict)
            session_var.name = pickle.dumps({'name':name,'project':'Homer Project'})
            if request.user.is_authenticated(): session_var.owner = request.user.profile
            session_var.save()
            
            request.session['request_id'] = request_id
            request.session['glossary_dict'] = glossary_dict
            request.session['select_table'] = select_table
            request.session.modified = True
            
            text_analyzed.send(sender=None, session_variable = session_var, request = request, text = content)
            
            if prepare == 'prepare':
                return HttpResponse(request_id)
            
            vocab_formset = initialize_vocab_formset(select_table, glossary_dict)
            session_var.initial_select_table = pickle.dumps(select_table)
            session_var.save()
            update_session(request, session_var)
            return render(request,'vocabs.html',{'formset':vocab_formset,'name_form':name_form,'title':'Vocabulary in'})
        else:
            return render(request,'errorPassage.html',{'error':form.errors})
    raise Http404        

     
def vocab_from_history(request,typ):
    try:
        session_var = SessionVariables.objects.get(request_id=request.session['request_id'])
    except:
         raise Http404
    update_session(request, session_var)
    name = pickle.loads(session_var.name)['name']
    project = pickle.loads(session_var.name)['project']
    request_id= request.session['request_id']
    name_form = NameForm(initial={'name':name,'project':project,'request_id':request_id},prefix='name')
    if typ != 'quiz':
        vocab_formset = initialize_vocab_formset(request.session['select_table'], request.session['glossary_dict'])
        return render(request,'vocabs.html',{'formset':vocab_formset,'name_form':name_form,'title':'Vocabulary in'})
    else: 
        if 'quiz_select_table' in request.session:
            vocab_formset = initialize_vocab_formset(request.session['quiz_select_table'], request.session['glossary_dict'])
        else:
            vocab_formset = initialize_vocab_formset(request.session['select_table'], request.session['glossary_dict'])
        return render(request,'vocabs.html',{'formset':vocab_formset,'name_form':name_form,'title':'Quiz for'})


def progress(request):
    request_id = ''
    if 'request_id' in request.GET: request_id=request.GET['request_id']
    session_var_list = SessionVariables.objects.filter(request_id=request_id)
    if session_var_list.count() > 0:
        return HttpResponse(round(session_var_list[0].progress,1))
    return HttpResponse(0.0)


def get_all_defs(request, gid):
    if request.method == 'POST':
        glossary_formset = initialize_glossary_formset(request, gid)
        request_id = json.loads(request.body)['request_id']
        session_var = SessionVariables.objects.get(request_id=request_id)   
        if request_id != request.session['request_id']:
            #print "updating session variables" 
            update_session(request, session_var)
        glossary = request.session['glossary_dict'][gid]
        concordance = []
        for c in glossary['concordance']:
            concordance.append(c.encode('utf-8'))   
        all_defs_got.send(sender=None, session_variable = session_var, request = request, lemmas = glossary['lemmas'])
        return render(request,'glossary_all_def.html',{'formset':glossary_formset,'concordance':concordance})
    raise Http404


def change_defs(request):
    select_table = json.loads(request.body)['new_table']
    request_id = select_table.pop('request_id', '')
    session_var = SessionVariables.objects.get(request_id=request_id)   
    if request_id != request.session['request_id']: update_session(request, session_var)
    glossary_dict = request.session['glossary_dict']
    select_table['selected'] = len(select_table['defs']) != 0
    group_select_table(glossary_dict, select_table)
    table_type = json.loads(request.body)['type']
    if request_id != request.session['request_id']:
        old_select_table = pickle.loads(getattr(session_var, table_type))
    else:
        old_select_table = request.session['select_table']
    for table_entry in old_select_table:
        if str(table_entry['gid']) == select_table['gid']:
            select_table['highlight']=table_entry['highlight']
            if select_table['selected']: 
                table_entry['defs'] = select_table['defs']
            else:
                select_table['defs'] = table_entry['defs']
            break
    setattr(session_var, table_type, pickle.dumps(old_select_table))
    session_var.save()
    request.session[table_type] = old_select_table
    request.session.modified = True
    
    vocab_formset = initialize_vocab_formset([select_table], glossary_dict)
    
    defs_changed.send(sender=None, session_variable = session_var, request = request, lemmas = glossary_dict[select_table['gid']]['lemmas'])
    return render(request,'vocabs_entry.html',{'formset':vocab_formset})


def add_lemma(request, gid):
    if json.loads(request.body)['lemma'] == '':
        return get_all_defs(request, gid)
    request_id = json.loads(request.body)['request_id']
    session_var = SessionVariables.objects.get(request_id=request_id)
    glossary_dict = pickle.loads(session_var.glossary_dict)
    glossary = glossary_dict[gid]
    from lexicon.views import Glossary, lemma
    tokens = glossary['tokens']
    lemmas = glossary['lemmas']  + lemma(json.loads(request.body)['lemma'])
    lemmas = list(set(lemmas))
    glossary = Glossary(tokens = {'lemmas':lemmas,'tokens':tokens}, gid = gid, concordance = glossary['concordance']).serialize()
    glossary_dict[gid] = glossary
    setattr(session_var, 'glossary_dict', pickle.dumps(glossary_dict))
    session_var.save()
    update_session(request, session_var)
    
    lemma_added.send(sender=None, request = request, tokens = tokens, lemmas = glossary['lemmas'], lemma = json.loads(request.body)['lemma'])
    return get_all_defs(request, gid)


def get_pdf(request, order = 'difficulty'):
    if request.method == 'POST':
        VocabFormSet = formset_factory(VocabForm,extra=0)
        vocab_formset = VocabFormSet(request.POST,prefix='vocab')
        name_form = NameForm(request.POST,prefix='name')
        if not (vocab_formset.is_valid() and name_form.is_valid()):
            raise Http404
        select_table = select_table_from_vocabfm(vocab_formset)
        request_id = name_form.cleaned_data['request_id']
        session_var = SessionVariables.objects.get(request_id=request_id)   
        setattr(session_var, 'select_table', pickle.dumps(select_table))
        session_var.name = pickle.dumps({'name':name_form.cleaned_data['name'],'project':name_form.cleaned_data['project']})
        session_var.save()
        if request_id != request.session['request_id']: update_session(request, session_var)
        request.session['select_table'] = select_table
        request.session.modified = True
        
        if order == 'random':
            r = random.random()
            shuffle(select_table, lambda: r)
        elif order == 'alphabetic':
            glossary_dict = pickle.loads(session_var.glossary_dict)
            select_table = sorted(select_table, key=lambda k: glossary_dict[k['gid']]['lemmas'][0].lower())
        
        vocab_formset = initialize_vocab_formset(select_table,pickle.loads(session_var.glossary_dict))
        context = {'vocab_formset':vocab_formset,'name_form':name_form}
        pdf, error, rendered_tpl = generate_pdf('vocab.tex', context)
        if(pdf != None):
            pdf_file = SimpleUploadedFile(name_form.cleaned_data['name']+'.pdf', pdf, content_type="application/pdf")
            f = TempFile(upload = pdf_file)
            if request.user.is_authenticated(): f.owner = request.user.profile
            f.save()
            
            r = HttpResponse(content_type='application/pdf')
            r.write(pdf)
            
            pdf_created.send(sender= VOCAB_PDF ,session_variable = session_var, request = request)
            return r
        else:
            return render(request,'errorPdf.html',{'error':error,'texfile':rendered_tpl})
    raise Http404


def quiz(request):
    if request.method == 'POST':
        VocabFormSet = formset_factory(VocabForm,extra=0)
        vocab_formset = VocabFormSet(request.POST,prefix='vocab')
        name_form = NameForm(request.POST,prefix='name')
        if not (vocab_formset.is_valid() and name_form.is_valid()):
            raise Http404
        select_table = select_table_from_vocabfm(vocab_formset, drop = True)
        request_id = name_form.cleaned_data['request_id']
        session_var = SessionVariables.objects.get(request_id=request_id)   
        if request_id != request.session['request_id']: update_session(request, session_var)
        setattr(session_var, 'quiz_select_table', pickle.dumps(select_table))
        session_var.save()
        request.session['quiz_select_table'] = select_table
        request.session.modified = True
        
        request_id = name_form.cleaned_data['request_id']
        session_var = SessionVariables.objects.get(request_id=request_id)
        vocab_formset = initialize_vocab_formset(select_table,pickle.loads(session_var.glossary_dict))
        
        quiz_created.send(sender=None,session_variable = session_var, request = request)
        return render(request,'vocabs.html',{'formset':vocab_formset,'name_form':name_form,'title':'Quiz for'})
    raise Http404        


def quiz_pdf(request):
    if request.method != 'POST': raise Http404
    VocabFormSet = formset_factory(VocabForm,extra=0)
    vocab_formset = VocabFormSet(request.POST,prefix='vocab')
    name_form = NameForm(request.POST,prefix='name')
    if not (vocab_formset.is_valid() and name_form.is_valid()):
        raise Http404
    select_table = select_table_from_vocabfm(vocab_formset)
    request_id = name_form.cleaned_data['request_id']
    session_var = SessionVariables.objects.get(request_id=request_id)   
    if request_id != request.session['request_id']: update_session(request, session_var)
    setattr(session_var, 'quiz_select_table', pickle.dumps(select_table))
    session_var.name = pickle.dumps({'name':name_form.cleaned_data['name'],'project':name_form.cleaned_data['project']})
    session_var.save()
    request.session['quiz_select_table'] = select_table
    request.session.modified = True
    if vocab_formset.is_valid() and name_form.is_valid():
        name_form = name_form.cleaned_data
        vocab_formset_raw =  vocab_formset.cleaned_data
        shuffle(vocab_formset_raw)
        vocab_formset=[]
        for vocab in vocab_formset_raw:
            if vocab['selected']:
                vocab_formset.append(vocab)
        alphabet = ['a','b','c','d','e','f','g','h','i','j']
        vocabs=[[[]]]
        defs=[[[]]]
        j=0
        k=0
        for i in range(len(vocab_formset)):
            vocab_formset[i].update({'number':i+1,'answer':alphabet[i % 10]})
            vocabs[j][k].append(vocab_formset[i])
            defs[j][k].append({'dict_def':vocab_formset[i]['dict_def'],'number':i+1})
            if(i % 30 == 29):
                vocabs.append([])
                defs.append([])
                try:
                    shuffle(vocabs[j][0])
                    shuffle(vocabs[j][1])
                    shuffle(vocabs[j][2])
                except:
                    pass
                j=j+1
                k=-1
            if(i % 10 == 9):
                vocabs[j].append([])
                defs[j].append([])
                k=k+1
        try:
            shuffle(vocabs[j][0])
            shuffle(vocabs[j][1])
            shuffle(vocabs[j][2])
        except:
            pass
        for i in range(len(vocabs)):
            for j in range(len(vocabs[i])):
                for k in range(len(vocabs[i][j])):
                    vocabs[i][j][k].update(defs[i][j][k])
        context = {'vocabs':vocabs,'name_form':name_form}
        qquiz, errorq, rendered_tplq = generate_pdf('quiz.tex', context)
        answer, errora, rendered_tpla = generate_pdf('answer.tex', context)
        if(qquiz!=None and answer!=None):
            z=zipf([{'name':name_form.name+'_quiz.pdf','file':qquiz},{'name':name_form.name+'_answer.pdf','file':answer}])
            response = HttpResponse(z, content_type='application/force-download')
            filename=name_form.name+'_quiz&answer'+id_generator(3)+'.zip'
            response['Content-Disposition'] = 'attachment; filename="%s"' % filename
            
            pdf_created.send(sender=QUIZ_PDF,session_variable = session_var, request = request)
            return response
        else:
            return render(request,'errorPdf.html',{'error':errorq+'\n'+errora,'texfile':rendered_tplq+'\n'+rendered_tpla})
    else:
        return render(request,'errorVocab.html',{'error':str(vocab_formset.errors)+'\n\n'+name_form.errors})

#////////////////////////////////////////////////////////////
# Select Vocab 
#////////////////////////////////////////////////////////////

def sort_select_table(glossary_dict, select_tabel, reverse = False):
    for i in range(len(select_tabel)-1):
        for j in range(len(select_tabel)-1):
            if not reverse and glossary_dict[select_tabel[j]['gid']]['difficulty'] > glossary_dict[select_tabel[j+1]['gid']]['difficulty']:
                temp =  select_tabel[j]
                select_tabel[j] = select_tabel[j+1]
                select_tabel[j+1]= temp
            if  reverse and glossary_dict[select_tabel[j]['gid']]['difficulty'] < glossary_dict[select_tabel[j+1]['gid']]['difficulty']:
                temp =  select_tabel[j]
                select_tabel[j] = select_tabel[j+1]
                select_tabel[j+1]= temp

             
def vocab_select(glossary_dict, request=None, dict_pref={'learner':1, 'collegiate':2}, show_cutoff = 4.3, diff_cutoff = 6):
    dict_pref={'learner':1, 'collegiate':2}
    show_cutoff = 4.3
    diff_cutoff = 6
    if request != None and request.user.is_authenticated():
        dict_pref = request.user.profile.vocab_preference.dict_pref
        show_cutoff = request.user.profile.vocab_preference.show_cutoff
        diff_cutoff = request.user.profile.vocab_preference.diff_cutoff
    
    select_table = []
    for gid, glossary in glossary_dict.iteritems():
      if glossary['difficulty'] > show_cutoff: 
        selected = glossary['difficulty'] >= diff_cutoff
        entry_id = ''
        pos_freq = copy.deepcopy(glossary['pos_freq'])
        highlight = False
        
        for j in range(len(pos_freq)):
            if j+1 < len(pos_freq) and pos_freq[j]['freq'] > pos_freq[j+1]['freq']:
                temp = pos_freq[j]
                pos_freq[j] = pos_freq[j+1]
                pos_freq[j+1] = temp
        
        if len(glossary['pos_list']) != 1:
         for pos in glossary['tokens_pos']:
            if 'V' in pos:
                if len(pos_freq)>0: highlight = pos_freq[-1]['pos'] != 'verb' and 'verb' in glossary['pos_list']
                for hw in glossary['lemmas']: pos_freq.append({'freq':1000, 'headword': hw, 'pos':'verb'})
            if not highlight and len(glossary['lemmas']) ==1 and 'NN' in pos:
                if pos == 'NN':
                    if len(pos_freq)>0: highlight = pos_freq[-1]['pos'] != 'noun' and pos_freq[-1]['headword'] == glossary['tokens'][0] and 'noun' in glossary['pos_list']
                    pos_freq.append({'freq':1000, 'headword': glossary['tokens'][0], 'pos':'noun'})
                else:
                    if len(pos_freq)>0: highlight = pos_freq[-1]['pos'] != 'noun' and 'noun' in glossary['pos_list']
                    for hw in glossary['lemmas']: pos_freq.append({'freq':1000, 'headword': hw, 'pos':'noun'})
         #if len(glossary['tokens_pos'])>1: highlight = True
        
        for i in range(len(pos_freq)):
            for j in range(len(pos_freq)):
                if j+1 < len(pos_freq) and pos_freq[j]['freq'] > pos_freq[j+1]['freq']:
                    temp = pos_freq[j]
                    pos_freq[j] = pos_freq[j+1]
                    pos_freq[j+1] = temp
            headword = pos_freq[j-i]['headword']
            pos = pos_freq[j-i]['pos']
            rank_top = 100
            for dict_type, rank in dict_pref.iteritems():
                if headword+','+dict_type+','+pos in glossary['pos_type_dict']:
                    if rank!=0 and rank < rank_top: 
                        rank_top = rank
                        entry_id = glossary['pos_type_dict'][headword+','+dict_type+','+pos]
            if entry_id != '': 
                select_table.append({'gid':gid,'selected':selected,'defs':[{'entry_id':entry_id, 'senses':['-1']}],'highlight':highlight})
                break
        
        if entry_id == '':
            rank_top = 100  
            for dict_type, rank in dict_pref.iteritems():
                for entry_list_id in glossary['entry_list']:
                    if dict_type in entry_list_id and rank < rank_top:
                        rank_top = rank
                        entry_id = entry_list_id
                        break
            select_table.append({'gid':gid,'selected':selected,'defs':[{'entry_id':entry_id, 'senses':['-1']}],'highlight':highlight})    
    sort_select_table(glossary_dict, select_table)
    return select_table


def group_select_table(glossary_dict, select_tabel):
    for entry in select_tabel['defs']:
        entry_pointer = EntryPointerQuery.objects.get(entry_id=entry['entry_id'])
        if entry_pointer == None: break
        entry['senses'] = entry_pointer.group_sense(entry['senses'] )


def select_table_from_vocabfm(vocab_formset, drop = False):
    vocabs = vocab_formset.cleaned_data
    select_table = []
    for vocab in vocabs:
        new_glossary = True
        gid = vocab['gid']
        entry_id = vocab['entry_id']
        sense_id = vocab['sense_id']
        selected = vocab['selected']
        highlight = vocab['highlight'] == 'True'
        for glossary in select_table:
            if glossary['gid'] == str(gid):
                new_glossary = False
                new_entry = True
                for def_ in glossary['defs']:
                    if def_['entry_id'] == entry_id:
                        def_['senses'].append(sense_id)
                        new_entry = False
                if new_entry:
                    glossary['defs'].append({'entry_id':entry_id, 'senses':[sense_id]})
        if new_glossary:
            select_table.append({'gid':str(gid),'selected':False,'highlight':highlight,'defs':[{'entry_id':entry_id, 'senses':[sense_id]}]})
    
    for vocab in vocabs:
        new_glossary = True
        gid = vocab['gid']
        entry_id = vocab['entry_id']
        sense_id = vocab['sense_id']
        selected = vocab['selected']
        if selected:
         for glossary in select_table:
            if glossary['gid'] == str(gid):
                new_glossary = False
                new_entry = True
                if not glossary['selected']: glossary['defs'] = []
                glossary['selected'] = True
                for def_ in glossary['defs']:
                    if def_['entry_id'] == entry_id:
                        def_['senses'].append(sense_id)
                        new_entry = False
                if new_entry:
                    glossary['defs'].append({'entry_id':entry_id, 'senses':[sense_id]})
    if not drop: return select_table
    select_table_drop = []
    for glossary in select_table:
        if glossary['selected']: select_table_drop.append(glossary)
    return select_table_drop

#////////////////////////////////////////////////////////////
# Initialize Vocab Form 
#////////////////////////////////////////////////////////////

def initialize_vocab_formset(select_table, glossary_dict):
    vocabs = []
    VocabFormSet = formset_factory(VocabForm,extra=0)
    for glossary in select_table:
        g_highligh = 'highlight' in glossary.keys() and glossary['highlight']
        for entry in glossary['defs']:
            entry_pointer = EntryPointerQuery.objects.get(entry_id=entry['entry_id'])
            if entry_pointer == None: break
            for n,sense in enumerate(entry['senses']):
                def_, vi, sense, high_light = entry_pointer.get_def_vi(sense)
                entry['senses'][n]=sense
                vocabs.append({
                    'selected':glossary['selected'],
                    'gid':glossary['gid'],
                    'entry_id':entry['entry_id'],
                    'highlight_selection': get_highlight_selection(glossary_dict, glossary, entry, sense, high_light or g_highligh),
                    'highlight':high_light or g_highligh,
                    'sense_id':sense,
                    'word':entry_pointer.headword,
                    'difficulty': round(glossary_dict[str(glossary['gid'])]['difficulty'],1),
                    'pospeech':entry_pointer.pos,
                    'dict_def':def_,
                    'sentence':vi,
                    'sentence_custom':vi,
                })
    vocab_formset =VocabFormSet(initial=vocabs,prefix='vocab')
    return vocab_formset


def get_highlight_selection(glossary_dict, glossary, entry, sense, high_light):
    #if len(glossary_dict[str(glossary['gid'])]['pos_list']) >2 or high_light: return 'def_menu-highlight'
    if high_light: return 'def_menu-highlight'
    if len(glossary_dict[str(glossary['gid'])]['pos_list']) == 1 : return ''
    return 'def_menu-multiple'


#////////////////////////////////////////////////////////////
# Initialize Glossary Form 
#////////////////////////////////////////////////////////////

def initialize_glossary_formset(request, gid):
    request_id= json.loads(request.body)['request_id']
    session_var = SessionVariables.objects.get(request_id=request_id)   
    if request_id != request.session['request_id']: update_session(request, session_var)
    glossary = request.session['glossary_dict'][str(gid)]
    gi = []
    for eid in glossary['entry_list']:
        ep = EntryPointer.objects.get(entry_id = eid)
        root = ET.fromstring(ep.data.encode('utf-8'))
        selected_sense = get_selected_sense(request, glossary, gid, eid)
        gi.append({
            'word':ep.headword,
            'gid':gid,
            'pospeech':ep.pos,
            'dict_type':ep.dict_type,
            'entry_id':eid,
            'data':stringify_children(root.find('def')),
            'selected_sense':selected_sense
        })
    gi = sort_glossary(glossary, gi)
    GlossaryFormSet = formset_factory(GlossaryDefForm,extra=0)
    glossary_formset = GlossaryFormSet(initial=gi)
    return glossary_formset


def get_selected_sense(request, glossary, gid, eid):
    request_id= json.loads(request.body)['request_id']
    session_var = SessionVariables.objects.get(request_id=request_id)   
    if request_id != request.session['request_id']: update_session(request, session_var)
    select_table = request.session['select_table']
    selected_sense = ''
    for select_entry in select_table:
        if select_entry['gid'] == str(gid):
            break
    for def_ in select_entry['defs']:
        if def_['entry_id'] == eid:
            if selected_sense !='': selected_sense=selected_sense+','
            selected_sense = selected_sense + ','.join(sense for sense in def_['senses'])
    return selected_sense


def sort_glossary(glossary, gi, dict_pref={'learner':1, 'collegiate':2}):
    new_gi=[]
    dict_pref_list=list(dict_pref.keys())
    for i in range(len(dict_pref_list)):
        for j in range(len(dict_pref_list)):
            if j+1 < len(dict_pref_list) and dict_pref[dict_pref_list[j]] > dict_pref[dict_pref_list[j+1]]:
                temp = dict_pref_list[j]
                dict_pref_list[j] = dict_pref_list[j+1]
                dict_pref_list[j+1] = temp
                
    for i in range(len(glossary['pos_freq'])):
        for j in range(len(glossary['pos_freq'])):
            if j+1 < len(glossary['pos_freq']) and glossary['pos_freq'][j]['freq'] < glossary['pos_freq'][j+1]['freq']:
                temp =  glossary['pos_freq'][j]
                glossary['pos_freq'][j] = glossary['pos_freq'][j+1]
                glossary['pos_freq'][j+1] = temp
    
    pos_freq = copy.deepcopy(glossary['pos_freq'])
    for entry in glossary['pos_freq']:
        headword = entry['headword']
        ll=[]
        for n, entry_inter in enumerate(pos_freq):
            if entry_inter['headword'] == headword:
                pos = entry_inter['pos']
                for dict_type in dict_pref_list:
                    l = []
                    for i, g in enumerate(gi):
                        if g['word'] == headword and g['pospeech'] == pos and g['dict_type']==dict_type:
                            new_gi.append(g)
                            l.insert(0,i)
                    for i in l: gi.pop(i)
                ll.insert(0,n)
        for i in ll: pos_freq.pop(i)
        gir = copy.deepcopy(gi)
        for g_inter in gir:
            if g_inter['word'] == headword:
                 pos = g_inter['pospeech']
                 for dict_type in dict_pref_list:
                     l = []
                     for i, g in enumerate(gi):
                         if g['word'] == headword and g['pospeech'] == pos and g['dict_type']==dict_type:
                             new_gi.append(g)
                             l.insert(0,i)
                     for i in l: gi.pop(i)
        if pos_freq == []: break
        
    if gi != []:
        gir = copy.deepcopy(gi)
        for g_inter in gir:
            headword = g_inter['word']
            pos = g_inter['pospeech']
            for dict_type in dict_pref_list:
                l = []
                for i, g in enumerate(gi):
                    if g['word'] == headword and g['pospeech'] == pos and g['dict_type']==dict_type:
                        new_gi.append(g)
                        l.insert(0,i)
                for i in l: gi.pop(i)
                   
    return new_gi

#////////////////////////////////////////////////////////////
# Session Variables Management
#////////////////////////////////////////////////////////////

def update_session(request, session_var):
    if session_var.request_id != '':
        request.session['request_id']=session_var.request_id
    if session_var.glossary_dict != None:
        request.session['glossary_dict']=pickle.loads(session_var.glossary_dict)
    if session_var.select_table != None:
        request.session['select_table']=pickle.loads(session_var.select_table)
    elif session_var.initial_select_table != None:
        request.session['select_table']=pickle.loads(session_var.initial_select_table)
    if session_var.quiz_select_table != None:
        request.session['quiz_select_table']=pickle.loads(session_var.quiz_select_table)
    request.session.modified = True
    return 

#////////////////////////////////////////////////////////////
# Generate Pdf
#////////////////////////////////////////////////////////////

def generate_pdf(template_file,context):
    template = get_template(template_file)
    rendered_tpl = template.render(context).encode('utf-8')
    rendered_tpl = html_decode(rendered_tpl)
    try:
        error = ""
        with TemporaryDirectory() as tempdir:
            for i in range(2):
                process = Popen(
                    ['pdflatex', '-output-directory', tempdir],
                    stdin=PIPE,
                    stdout=PIPE,
                )
                process.communicate(rendered_tpl)
            with open(_os.path.join(tempdir, 'texput.log'), 'rb') as f:
                error = f.read()
            with open(_os.path.join(tempdir, 'texput.pdf'), 'rb') as f:
                pdf = f.read()
        return pdf, error, rendered_tpl
    except:
        return None, error, rendered_tpl

#////////////////////////////////////////////////////////////
# Utilities 
#////////////////////////////////////////////////////////////

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    import random
    return ''.join(random.choice(chars) for i in range(size))


def html_decode(s):
    """
    Returns the ASCII decoded version of the given HTML string. This does
    NOT remove normal HTML tags like <p>.
    """
    htmlCodes = (
            ("'", '&#39;'),
            ('"', '&quot;'),
            ('>', '&gt;'),
            ('<', '&lt;'),
            ('\&', '&amp;'),
            ('\$','$')
        )
    for code in htmlCodes:
        s = s.replace(code[1], code[0])
    return s


class TemporaryDirectory(object):
    """Create and return a temporary directory.  This has the same
    behavior as mkdtemp but can be used as a context manager.  For
    example:

        with TemporaryDirectory() as tmpdir:
            ...

    Upon exiting the context, the directory and everything contained
    in it are removed.
    """
    
    def __init__(self, suffix="", prefix="tmp", dir=None):
        self._closed = False
        self.name = None # Handle mkdtemp raising an exception
        self.name = mkdtemp(suffix, prefix, dir)

    def __repr__(self):
        return "<{} {!r}>".format(self.__class__.__name__, self.name)

    def __enter__(self):
        return self.name

    def cleanup(self, _warn=False):
        if self.name and not self._closed:
            try:
                self._rmtree(self.name)
            except (TypeError, AttributeError) as ex:
                # Issue #10188: Emit a warning on stderr
                # if the directory could not be cleaned
                # up due to missing globals
                if "None" not in str(ex):
                    raise
                #print("ERROR: {!r} while cleaning up {!r}".format(ex, self,),file=_sys.stderr)
                return
            self._closed = True
            if _warn:
                self._warn("Implicitly cleaning up {!r}".format(self),
                           ResourceWarning)

    def __exit__(self, exc, value, tb):
        self.cleanup()

    def __del__(self):
        # Issue a ResourceWarning if implicit cleanup needed
        self.cleanup(_warn=True)

    # XXX (ncoghlan): The following code attempts to make
    # this class tolerant of the module nulling out process
    # that happens during CPython interpreter shutdown
    # Alas, it doesn't actually manage it. See issue #10188
    _listdir = staticmethod(_os.listdir)
    _path_join = staticmethod(_os.path.join)
    _isdir = staticmethod(_os.path.isdir)
    _islink = staticmethod(_os.path.islink)
    _remove = staticmethod(_os.remove)
    _rmdir = staticmethod(_os.rmdir)
    _warn = _warnings.warn

    def _rmtree(self, path):
        # Essentially a stripped down version of shutil.rmtree.  We can't
        # use globals because they may be None'ed out at shutdown.
        for name in self._listdir(path):
            fullname = self._path_join(path, name)
            try:
                isdir = self._isdir(fullname) and not self._islink(fullname)
            except OSError:
                isdir = False
            if isdir:
                self._rmtree(fullname)
            else:
                try:
                    self._remove(fullname)
                except OSError:
                    pass
        try:
            self._rmdir(path)
        except OSError:
            pass


def zipf(files,zfname='quiz&answer'):
    with TemporaryDirectory() as dst:
        zf = zipfile.ZipFile("%s.zip" % (_os.path.join(dst, zfname)), "w", zipfile.ZIP_DEFLATED)
        for ffile in files:
            try:
                name=ffile['name']
                f_file=ffile['file']
            except:
                name=ffile.name
                f_file=ffile.read()
            zf.writestr(name,f_file)
        zf.close()
        z = open(_os.path.join(dst, zfname+'.zip'), 'r')
        return z
