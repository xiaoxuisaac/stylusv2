from lexicon.models import *
import urllib2
import lxml.etree as ET
from lxml.etree import tostring
from itertools import chain
import re
#from rebuild import export_learner, export
from difflib import SequenceMatcher
from lexicon.models import *

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

     
def clear_learner_pointer():
    for entry in LearnerEntryPointer.objects.all():
        entry.delete()

def learner_from_coca(lower,upper):
    i = lower
    while i < upper:
        print i
        i+=1
        w = CocaFreq.objects.get(rank = i).headword
        add_learner(w)

def add_learner(word):
    word = word.lower()
    raw, created = LearnerRaw.objects.get_or_create(alpha=word.lower())
    #print created
    added = False
    if(created or raw.data == ''):
        print("New Word from Learner Website: "+word.encode('utf-8'))
        response = urllib2.urlopen('http://www.dictionaryapi.com/api/v1/references/learners/xml/'
              +word.encode('utf-8')+'?key=40d96316-f219-4661-893b-62df83769d28')

        raw.data = response.read().decode('utf-8')
        raw.save()
    try:
        root = ET.fromstring(raw.data.encode('utf-8'))
    except:
        return added
    for xml_entry in root.findall('entry'):
        if ' ' not in xml_entry.get('id') and not xml_entry.get('id')[0].isupper():
            add_learner_pointer(xml_entry)
            added = True
    return added

#////////////////////////////////////////////////////////////
# Add a entry pointer structure
#//////////////////////////////////////////////////////////// 

def add_learner_pointer(xml_entry):
    #print stringify_children(xml_entry)
    entry_pointer,created = EntryPointer.objects.get_or_create(entry_id='learner-' + xml_entry.get('id'))
    if not created:
        #print("entry_data "+xml_entry.get('id')+" already exists.")
        return
    entry_pointer.dict_type = 'learner'
    entry_pointer.type_id = xml_entry.get('id')
    entry_pointer.headword = xml_entry.find('hw').text.replace("*","").replace(" ","").lower()
    pos = xml_entry.find('fl')
    if pos is not None:
        entry_pointer.pos = pos.text.replace("*","").replace(" ","").lower()
    word_pointer,created = WordPointer.objects.get_or_create(word=entry_pointer.headword)
    #if created: print xml_entry.find('hw').text.replace("*","").replace(" ","").lower() + ' create word pointer '+entry_pointer.headword
    entry_pointer.word_pointer = word_pointer
    
    #print entry_pointer
    #print stringify_children(xml_entry)
    #print xml_entry.find('def') is not None
    if xml_entry.find('def') is not None:
        entry_pointer.derivations.add(word_pointer)
        entry_pointer.has_def = True
        #print word_pointer
        
    for der in xml_entry.findall('vr/va'):
        word_pointer,created = WordPointer.objects.get_or_create(word=der.text.replace("*","").replace(" ","").lower())
     #   if created: 
     #       print 'create word pointer '+ der.text
     #       print word_pointer
     #   print word_pointer
     #   print der.text+' '+entry_pointer.headword+' vr/va'
        entry_pointer.derivations.add(word_pointer)
        
    for der in xml_entry.findall('in/if'):
        word_pointer,created = WordPointer.objects.get_or_create(word=der.text.replace("*","").replace(" ","").lower())
    #    print 'wp '+der.text.replace("*","").replace(" ","").lower()
    #    print word_pointer
    #    if created: 
    #        print 'create word pointer '+ der.text
    #        print word_pointer
    #    print der.text+' '+entry_pointer.headword+' in/if'
        entry_pointer.derivations.add(word_pointer)
            
    for der in xml_entry.findall('uro/ure'):
        word_pointer,created = WordPointer.objects.get_or_create(word=der.text.replace("*","").replace(" ","").lower())
    #    if created: 
    #        print 'create word pointer '+ der.text
    #        print word_pointer
    #    print der.text+' '+entry_pointer.headword+' uro/ure'
        entry_pointer.derivations.add(word_pointer)
        
    for der in xml_entry.findall('uro/in/if'):
        word_pointer,created = WordPointer.objects.get_or_create(word=der.text.replace("*","").replace(" ","").lower())
    #    if created: 
    #        print 'create word pointer '+ der.text
    #        print word_pointer
    #    print der.text+' '+entry_pointer.headword+' uro/in/if'
        entry_pointer.derivations.add(word_pointer)
            
    for der in xml_entry.findall('uro/vr/va'):
        word_pointer,created = WordPointer.objects.get_or_create(word=der.text.replace("*","").replace(" ","").lower())
    #    if created: 
    #        print 'create word pointer '+ der.text
    #        print word_pointer
    #    print der.text+' '+entry_pointer.headword+' uro/ure/vr/va'
        entry_pointer.derivations.add(word_pointer)
        
    for der in xml_entry.findall('cx/ct'):
        word_pointer,created = WordPointer.objects.get_or_create(word=der.text.replace("*","").replace(" ","").lower())
        #if created: 
        #    print 'create word pointer '+ der.text
        #    print word_pointer
        if xml_entry.find('def') is not None:
        #    print der.text+' '+entry_pointer.headword+' cx/ct'
            entry_pointer.derivations.add(word_pointer)
    #print entry_pointer.derivations.all()
    entry_pointer.save()
    for wp in entry_pointer.derivations.all():
        wp.update_lemmas()
        wp.save()
    entrydata = EntryData.objects.create(entry_id=entry_pointer.entry_id, pointer=entry_pointer,
                                            dict_type=entry_pointer.dict_type, type_id = entry_pointer.type_id)
    entrydata.headword =  entry_pointer.headword
    entrydata.data = '<entry>'+stringify_children(xml_entry)+'</entry>'
    entrydata.save()
               
#////////////////////////////////////////////////////////////
# Utilities
#////////////////////////////////////////////////////////////  

def stringify_children(node):
    parts = ([node.text.encode('utf-8') if node.text else None] +
            list(chain(*([tostring(c,encoding='UTF-8')] for c in node.getchildren()))))# +
            #[node.tail.encode('utf-8') if node.tail else None])
    return ''.join(filter(None, parts))