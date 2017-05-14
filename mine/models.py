from __future__ import unicode_literals

from django.db import models
from django.dispatch import receiver
from gargoyle.signals import *
from ums.models import Profile

from django.utils import timezone

# Create your models here.

class VocabVariables(models.Model):
    request_id = models.CharField(max_length=125, primary_key=True)
    created_date = models.DateTimeField(editable=False, default=timezone.now)
    name = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(Profile, related_name='mining_vocab_variables', null=True, blank=True)
    glossary_dict = models.TextField(blank=True, null=True)
    initial_select_table = models.TextField(blank=True, null=True)
    select_table = models.TextField(blank=True, null=True)
    quiz_select_table = models.TextField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    
    
@receiver(text_analyzed)
def save_vocab_variables_text(sender, request, session_variable, text, **kwargs):
    var, created = VocabVariables.objects.get_or_create(request_id = session_variable.request_id)
    var.name = session_variable.name
    if session_variable.owner != None:  var.owner = session_variable.owner
    if session_variable.glossary_dict != None: var.glossary_dict = session_variable.glossary_dict
    if session_variable.initial_select_table != None: var.initial_select_table = session_variable.initial_select_table
    var.text = text
    var.save()
    
@receiver(pdf_created, sender=VOCAB_PDF)
def save_vocab_variables_vocab(sender, request, session_variable, **kwargs):
    var, created = VocabVariables.objects.get_or_create(request_id = session_variable.request_id)
    var.name = session_variable.name
    if session_variable.owner != None:  var.owner = session_variable.owner
    if session_variable.glossary_dict != None: var.glossary_dict = session_variable.glossary_dict
    if session_variable.initial_select_table != None: var.initial_select_table = session_variable.initial_select_table
    if session_variable.select_table != None: var.select_table = session_variable.select_table
    var.save()
    
@receiver(pdf_created, sender=QUIZ_PDF)
def save_vocab_variables_quiz(sender, request, session_variable, **kwargs):
    var, created = VocabVariables.objects.get_or_create(request_id = session_variable.request_id)
    var.name = session_variable.name
    if session_variable.owner != None:  var.owner = session_variable.owner
    if session_variable.glossary_dict != None: var.glossary_dict = session_variable.glossary_dict
    if session_variable.initial_select_table != None: var.initial_select_table = session_variable.initial_select_table
    if session_variable.quiz_select_table != None: var.quiz_select_table = session_variable.quiz_select_table
    var.save()