from __future__ import unicode_literals
import string
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from gargoyle.signals import *

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile',on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    school = models.CharField(max_length=100, blank=True)
    invitor = models.ForeignKey('Profile', related_name='invitees', blank=True,null=True)
    invitation = models.CharField(max_length=30, blank=True,null=True)
    invite_code = models.CharField(max_length=30, blank=True,null=True)
    def save(self, *args, **kwargs):
        if not self.id:
            self.invitation=self.invitation=id_generator(5)
        flag=True
        while flag:
            flag=False
            ps=Profile.objects.filter(invitation=self.invitation)
            if ps.count()>0 and ps[0]!=self:
                self.invitation=id_generator(5)
                flag=True
        return super(Profile, self).save(*args, **kwargs)
    
    def get_pwd_reset_link(self):
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        from django.contrib.auth.tokens import default_token_generator
        from django.urls import reverse
        token_generator=default_token_generator
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = token_generator.make_token(self.user)
        return reverse('password_reset_confirm', kwargs={'uidb64':uid, 'token':token})
    pwd_reset_link = property(get_pwd_reset_link)
    
    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
        

class AnalyzedVocabVariables(models.Model):
    request_id = models.CharField(max_length=125, primary_key=True)
    created_date = models.DateTimeField(editable=False, default=timezone.now)
    name = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(Profile, related_name='analyzed_vocab_variables')
    glossary_dict = models.TextField(blank=True, null=True)
    initial_select_table = models.TextField(blank=True, null=True)
    select_table = models.TextField(blank=True, null=True)
    quiz_select_table = models.TextField(blank=True, null=True)
    show = models.BooleanField(default=True)

@receiver(pdf_created)
def save_vocab_variables(sender, request, session_variable, **kwargs):
    if session_variable.owner == None: return 
    var, created = AnalyzedVocabVariables.objects.get_or_create(request_id = session_variable.request_id, owner = session_variable.owner)
    var.name = session_variable.name
    if session_variable.glossary_dict != None: var.glossary_dict = session_variable.glossary_dict
    if session_variable.initial_select_table != None: var.initial_select_table = session_variable.initial_select_table
    if session_variable.select_table != None: var.select_table = session_variable.select_table
    if session_variable.quiz_select_table != None: var.quiz_select_table = session_variable.quiz_select_table
    var.save()
    

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    import random
    return ''.join(random.choice(chars) for i in range(size))
  