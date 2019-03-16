from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.dispatch import receiver
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required,user_passes_test

from django.http import HttpResponse, Http404, HttpResponseRedirect


from .forms import *
from signals import *
from registration.backends.hmac.views import RegistrationView as RegistrationBaseView

import pickle
import datetime
from datetime import timedelta


# Create your views here.

class StylusRegistrationView(RegistrationBaseView):
     """
     Register a new (inactive) user account, generate and store an
     activation key, and email it to the user.

     """
    
     @method_decorator(csrf_exempt)
     def dispatch(self, request, *args, **kwargs):
        #logger.info(get_ip(request)+' Registered User ')
        return super(StylusRegistrationView, self).dispatch(request, *args, **kwargs)
                
     def register(self, form):
        new_user = self.create_inactive_user(form)
        new_user.is_active = True
        new_user.save()
        code=form.cleaned_data['invitation']
        new_user.profile.invite_code = code
        new_user.profile.save()
         
        user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=self.request)

        ps=Profile.objects.filter(invitation=code)
        if ps.count()>0:
            new_user.profile.invitor = ps[0]
            new_user.save()
        
        User = get_user_model()
            
        new_user1 = authenticate(
            username=getattr(new_user, User.USERNAME_FIELD),
            password=form.cleaned_data['password1']
        )
        login(self.request, new_user1)
        
        return new_user

     def get_form_kwargs(self):
        kwargs = super(StylusRegistrationView, self).get_form_kwargs()
        kwargs.update(self.kwargs)  # self.kwargs contains all url conf param
        return kwargs
    
     def get_success_url(self, user):
        if True:
            return ('/',(),{})
        return ('registration_complete', (), {})
        
        
@user_passes_test(lambda u: u.is_authenticated())
def profile(request,load_url='vocab_history'):
    try:
        load_url=reverse(load_url)
    except:
        load_url=reverse('vocab_history')
    return render(request,'profile.html',{'load_url':load_url})
    
@user_passes_test(lambda u: u.is_authenticated())
def vocab_history(request):
    vocabs=[]
    import hashlib
    for variables in request.user.profile.analyzed_vocab_variables.order_by('-created_date'):
        name = pickle.loads(variables.name)
        if variables.select_table != None:
            select_table = pickle.loads(variables.select_table)
        elif variables.quiz_select_table != None:
            select_table = pickle.loads(variables.quiz_select_table)
        else:
            select_table = pickle.loads(variables.initial_select_table)
        count = 0    
        for s in select_table:
            if s['selected']: count += 1
        try:
            code = hashlib.sha224(variables.request_id).hexdigest()[-7:]
        except:
            code = 'none'
        time = {'year':variables.created_date.year, 'month':variables.created_date.strftime("%B"),'day':variables.created_date.day}
        if variables.show: vocabs.append({'code':code, 'time':time,'counter':count,'name':name})
    ocrs=[]
    for ocr in request.user.profile.ocr_files.order_by('-saved_date'):
        time = {'year':ocr.saved_date.year, 'month':ocr.saved_date.strftime("%B"),'day':ocr.saved_date.day}
        not_expire = datetime.datetime.today().replace(tzinfo=None) - timedelta(days=7) < ocr.saved_date.replace(tzinfo=None)
        if not_expire and ocr.show: ocrs.append({'time':time,'file':ocr})
    return render(request,'vocab_history_lean.html',{'vocabs':vocabs,'ocrs':ocrs})

@user_passes_test(lambda u: u.is_authenticated())    
def get_vocab(request):
    import hashlib
    code = ''
    duplicate = 'False'
    typ = 'vocab'
    if 'code' in request.GET: code=request.GET['code']
    if 'duplicate' in request.GET: duplicate=request.GET['duplicate']
    if 'typ' in request.GET: typ=request.GET['typ']
    for variables in request.user.profile.analyzed_vocab_variables.all():
         hash_code = hashlib.sha224(variables.request_id).hexdigest()[-7:]
         if hash_code == code:
             if duplicate == "False":
                 request.session['request_id']=variables.request_id
             else:
                 from gargoyle.views import id_generator
                 name = pickle.loads(variables.name)['name']
                 request.session['request_id'] = '|'.join([variables.owner.user.get_username(),datetime.date.today().isoformat(),name,id_generator()])
             request.session.modified = True
             from gargoyle.views import vocab_from_history
             from gargoyle.models import SessionVariables
             session_var = SessionVariables(request_id=request.session['request_id'])  
             session_var.glossary_dict = variables.glossary_dict
             session_var.name = variables.name
             session_var.owner = variables.owner
             session_var.select_table = variables.select_table
             session_var.initial_select_table = variables.initial_select_table
             if duplicate == 'True':
                 session_var.initial_select_table = variables.select_table
             session_var.quiz_select_table = variables.quiz_select_table
             session_var.save()
             retrieved_from_history.send(sender=None, session_variable = session_var, request = request, duplicate=duplicate,typ=typ)
             return vocab_from_history(request,typ)
    return Http404

@user_passes_test(lambda u: u.is_authenticated())      
def delete_vocab(request):
    import hashlib
    code = ''
    if 'code' in request.GET: code=request.GET['code']
    for variables in request.user.profile.analyzed_vocab_variables.all():
         hash_code = hashlib.sha224(variables.request_id).hexdigest()[-7:]
         if hash_code == code:
             variables.show=False
             variables.save()
             break
    return profile(request,load_url='vocab_history')
    
@user_passes_test(lambda u: u.is_authenticated())
def preference(request):
    from gargoyle.forms import VocabPreferenceForm
    from gargoyle.models import VocabPreference
    if request.method == 'POST':
        vocab_preference_form = VocabPreferenceForm(request.POST,instance=request.user.profile.vocab_preference, prefix="vocab")
        if vocab_preference_form.is_valid():
            vocab_preference_form.save()
        return render(request,'preference_lean.html',{'vocab_preference_form':vocab_preference_form})
    vocab_preference_form = VocabPreferenceForm(instance=request.user.profile.vocab_preference, prefix="vocab")
    return render(request,'preference_lean.html',{'vocab_preference_form':vocab_preference_form})