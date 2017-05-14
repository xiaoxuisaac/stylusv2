from __future__ import unicode_literals

from django.db import models
from django.dispatch import receiver

from gargoyle.signals import *
from ums.models import Profile
from ums.signals import *
from ocr.signals import *

from django.utils import timezone
from ipware.ip import get_ip
import json
import pickle

# Create your models here.

class LogData(models.Model):
    created_date = models.DateTimeField(editable=False, default=timezone.now)
    ip_addr = models.CharField(max_length=50)
    request_type = models.CharField(max_length=50)
    owner = models.ForeignKey(Profile, related_name='log_data', null=True, blank=True)
    info = models.CharField(max_length=200)
    note = models.CharField(max_length=200)
    
@receiver(file_ocred)
def ocr_log(sender, request, name, pages, url, **kwargs):
    log = LogData()
    log.ip_addr = get_ip(request) 
    log.request_type = 'ocr'
    if request.user.is_authenticated(): log.owner = request.user.profile
    log.info = 'OCRed file ' + name + ' , '+str(pages)+' pages '+url
    log.save()

@receiver(text_analyzed)
def text_analyzed_log(sender, request, session_variable, text, **kwargs):
    log = LogData()
    log.ip_addr = get_ip(request) 
    log.request_type = 'text_analyzed'
    if request.user.is_authenticated(): log.owner = request.user.profile
    log.info = 'Analyzed text ' +  pickle.loads(session_variable.name)['name']
    log.note = session_variable.request_id
    log.save()
    
@receiver(pdf_created, sender = VOCAB_PDF)
def vocab_pdf_log(sender, request, session_variable, **kwargs):
    log = LogData()
    log.ip_addr = get_ip(request) 
    log.request_type = 'vocab_pdf'
    if request.user.is_authenticated(): log.owner = request.user.profile
    select_table = pickle.loads(session_variable.select_table)
    count = 0    
    for s in select_table:
        if s['selected']: count += 1
    log.info = 'Export Vocab PDF, ' + str(count) + ' Words, for '+ pickle.loads(session_variable.name)['name']
    log.note = session_variable.request_id
    log.save()

@receiver(pdf_created, sender = QUIZ_PDF)
def quiz_pdf_log(sender, request, session_variable, **kwargs):
    log = LogData()
    log.ip_addr = get_ip(request) 
    log.request_type = 'vocab_pdf'
    if request.user.is_authenticated(): log.owner = request.user.profile
    select_table = pickle.dumps(session_variable.quiz_select_table)
    count = 0
    for s in select_table:
        if s['selected']: count += 1
    log.info = 'Export Quiz PDF, ' + str(count) + ' Words, for'+pickle.loads(session_variable.name)['name']
    log.note = session_variable.request_id
    log.save()
    
@receiver(lemma_added)
def lemma_added_log(sender, request, tokens, lemmas, lemma, **kwargs):
    log = LogData()
    log.ip_addr = get_ip(request) 
    log.request_type = 'lemma_added'
    if request.user.is_authenticated(): log.owner = request.user.profile
    log.info = 'Add lemma ' + lemma + ' to [' + ','.join(lemmas) +'] , [' + ','.join(tokens)+']'
    log.save()
    
@receiver(all_defs_got)
def all_defs_got_log(sender,lemmas, request, session_variable, **kwargs):
    log = LogData()
    log.ip_addr = get_ip(request) 
    log.request_type = 'all_defs_got'
    if request.user.is_authenticated(): log.owner = request.user.profile
    log.info = 'Get all Defs [' + ','.join(lemmas) +']'
    log.note = session_variable.request_id
    log.save()
    
@receiver(defs_changed)
def defs_changed_log(sender,lemmas, request, session_variable, **kwargs):
    log = LogData()
    log.ip_addr = get_ip(request) 
    log.request_type = 'defs_changed_got'
    if request.user.is_authenticated(): log.owner = request.user.profile
    log.info = 'Defs Changed [' + ','.join(lemmas) +']'
    log.note = session_variable.request_id
    log.save()
    
@receiver(user_registered)
def user_registered_log(sender, user, request, **kwargs):
    log = LogData()
    log.ip_addr = get_ip(request) 
    log.request_type = 'user_registered'
    if request.user.is_authenticated(): log.owner = request.user.profile
    log.info = 'User Registered ' + user.username
    log.save()
    
@receiver(retrieved_from_history)
def retrieved_from_history_log(sender, session_variable, request, duplicate, typ,  **kwargs):
    log = LogData()
    log.ip_addr = get_ip(request) 
    log.request_type = 'retrieved_from_history duplicate=' + duplicate
    if request.user.is_authenticated(): log.owner = request.user.profile
    log.info = 'Retrieved '+typ+' from History, duplicate = ' + duplicate
    log.save()
    
