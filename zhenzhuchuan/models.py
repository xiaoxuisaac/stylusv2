from __future__ import unicode_literals

from django.db import models

from lexicon.models import WordPointer
from ums.models import Profile
# Create your models here.
class WordListAbstract(models.Model):
    class Meta:
           abstract = True
           
    name = models.CharField(max_length=100, blank=True, null=True)
    glossary_dict = models.TextField(blank=True, null=True)
    select_table = models.TextField(blank=True, null=True)
    
class PrivateWordList(WordListAbstract):
    owner = models.ForeignKey(Profile, blank=True, null=True, related_name='public_wordlist')
    words = models.ManyToManyField(WordPointer)
    
class PublicWordList(WordListAbstract):
    words = models.ManyToManyField(WordPointer, related_name='private_wordlist')
    owner = models.ForeignKey(Profile, blank=True, null=True, related_name='private_wordlist')
    note = models.TextField(blank=True, null=True)
    published =  models.BooleanField(default=True, related_name='public_wordlist')
    
    