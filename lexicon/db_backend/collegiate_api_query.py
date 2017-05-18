from lexicon.models import *
import urllib2
import lxml.etree as ET
from lxml.etree import tostring
from itertools import chain
import re
#from rebuild import export_collegiate, export
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def clear_collegiate_pointer():
    for entry in CollegiateEntryPointer.objects.all():
        entry.delete()
        
def collegiate_from_coca(lower,upper):
    i = lower
    while i < upper:
        print i
        i+=1
        w = CocaFreq.objects.get(rank = i).headword
        #print w
        add_collegiate(w)

def add_collegiate(word):
    word = word.lower()
    added = False
    raw, created = CollegiateRaw.objects.get_or_create(alpha=word.lower())
    if(created or raw.data == ''):
        print("New Word from Collegiate Website: "+word.decode('utf-8'))
        response = urllib2.urlopen('http://www.dictionaryapi.com/api/v1/references/collegiate/xml/'
              +word.encode('utf-8')+'?key=11f82c71-15d3-4d60-ba76-6c2a62b57a0a')
        try:
            raw.data = response.read().decode('utf-8')
        except:
            return added
        raw.save()
    try:
        root = ET.fromstring(raw.data.encode('utf-8'))
    except:
        return added
    for xml_entry in root.findall('entry'):
        #print xml_entry.get('id').isupper()
        #print xml_entry.get('id')
        if ' ' not in xml_entry.get('id') and not xml_entry.get('id')[0].isupper():
            #print xml_entry.get('id')
            add_collegiate_pointer(xml_entry)
            added = True
    return added
#////////////////////////////////////////////////////////////
# Add a entry pointer structure
#//////////////////////////////////////////////////////////// 

def add_collegiate_pointer(xml_entry):
    entry_pointer,created = EntryPointer.objects.get_or_create(entry_id='collegiate-' + xml_entry.get('id'))
    if not created:
        #print("entry_data "+xml_entry.get('id')+" already exists.")
        return
    entry_pointer.dict_type = 'collegiate'
    entry_pointer.type_id = xml_entry.get('id')    
    ew = xml_entry.find('ew')
    if ew is None:
        entry_pointer.delete()
#        entry_pointer.save()
        return
    pos = xml_entry.find('fl')
    if pos is not None:
        entry_pointer.pos = pos.text.replace("*","").replace(" ","").lower()
    entry_pointer.headword = xml_entry.find('ew').text.replace("*","").lower()
    word_pointer,created = WordPointer.objects.get_or_create(word=entry_pointer.headword)
    entry_pointer.word_pointer = word_pointer
    
    if xml_entry.find('def') is not None:
        entry_pointer.derivations.add(word_pointer)
        entry_pointer.has_def = True
    
    for der in xml_entry.findall('vr/va'):
        word_pointer,created = WordPointer.objects.get_or_create(word=der.text.replace("*","").replace(" ","").lower())
        entry_pointer.derivations.add(word_pointer)
        
    for der in xml_entry.findall('in/if'):
        word_pointer,created = WordPointer.objects.get_or_create(word=der.text.replace("*","").replace(" ","").lower())
        entry_pointer.derivations.add(word_pointer)
            
    for der in xml_entry.findall('uro/ure'):
        word_pointer,created = WordPointer.objects.get_or_create(word=der.text.replace("*","").replace(" ","").lower())
        entry_pointer.derivations.add(word_pointer)
        
    for der in xml_entry.findall('uro/in/if'):
        word_pointer,created = WordPointer.objects.get_or_create(word=der.text.replace("*","").replace(" ","").lower())
        entry_pointer.derivations.add(word_pointer)
            
    for der in xml_entry.findall('uro/vr/va'):
        word_pointer,created = WordPointer.objects.get_or_create(word=der.text.replace("*","").replace(" ","").lower())
        entry_pointer.derivations.add(word_pointer)
        
    for der in xml_entry.findall('cx/ct'):
        word_pointer,created = WordPointer.objects.get_or_create(word=der.text.replace("*","").replace(" ","").lower())
        if xml_entry.find('def') is not None:
            entry_pointer.derivations.add(word_pointer)
            
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
            list(chain(*([tostring(c,encoding='UTF-8')] for c in node.getchildren()))) )#+
            #[node.tail.encode('utf-8') if node.tail else None])
    return ''.join(filter(None, parts))