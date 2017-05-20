from .models import *
from django import forms
import datetime
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from .widgets import TextDiv, DefMenuIcon, DictLogo
from django_select2.forms import Select2Widget


class PassageForm(forms.Form):
    name = forms.CharField(required=False,label="Text Name",max_length=100,widget=forms.TextInput(attrs={'class':'form-control text-name'}))
    request_id = forms.CharField(required=False,max_length=100,widget=forms.TextInput(attrs={'hidden':'true'}))
    content = forms.CharField(label="Text Content", max_length=1000000,widget=forms.Textarea(attrs={'class':'form-control project-name','rows':17, 'id':'home-content'}))

class NameForm(forms.Form):
    name = forms.CharField(required=False,label="Text Name",max_length=100,widget=forms.TextInput(attrs={'size':15}))
    project = forms.CharField(label="Project Name",max_length=100,widget=forms.TextInput(attrs={'size':13}))
    request_id = forms.CharField(required=False,label="Request Id",max_length=100,widget=forms.HiddenInput())
    
class FilesForm(forms.Form):
    upload = forms.FileField(widget=forms.ClearableFileInput(attrs={'class':'inputfile','multiple': False}))

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name','email','content']
        widgets = {
                   'name': forms.TextInput(attrs={'class':'form-control','size':20}),
                   'email': forms.TextInput(attrs={'class':'form-control','size':20}),
                   'content': forms.Textarea(attrs={'class':'form-control','rows':13}),
               }

class VocabForm(forms.Form):
    selected = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class':'counter'}))
    gid = forms.IntegerField(required=True,widget=forms.HiddenInput(attrs={'class':'input-gid'}))
    entry_id = forms.CharField(required=True,widget=forms.HiddenInput(attrs={'class':'input-entry_id'}))
    sense_id = forms.CharField(required=True,widget=forms.HiddenInput(attrs={'class':'input-sense_id'}))
    highlight = forms.CharField(required=True, initial= 'False',widget=forms.HiddenInput(attrs={'class':'input-highlight'}))
    
    word = forms.CharField(widget=TextDiv(attrs={'class':'input-word text-select'}))
    difficulty = forms.DecimalField(max_digits=4, decimal_places=2,widget=TextDiv(attrs={'class':'input-difficulty text-select'}))
    
    highlight_selection = forms.CharField(required=False,widget=DefMenuIcon())
    ipa =  forms.CharField(required=False,max_length=100)    
    pospeech =  forms.CharField(required=False,max_length=40,widget=TextDiv(attrs={'size':4,'class':'input-pospeech text-select'}))    
    dict_def = forms.CharField(required=False,widget=TextDiv(attrs={'size':40,'class':'input-webster_def text-select'}))
    sentence = forms.CharField(required=False,widget=TextDiv(attrs={'size':40,'class':'input-sentence text-select'}))
    sentence_custom = forms.CharField(required=False,widget=forms.HiddenInput())
    
class GlossaryDefForm(forms.Form):
    word = forms.CharField(widget=TextDiv(attrs={'class':'input-word text-select'}))
    gid = forms.IntegerField(required=True,widget=forms.HiddenInput(attrs={'class':'input-gid'}))
    entry_id = forms.CharField(required=True,widget=forms.HiddenInput(attrs={'class':'input-entry_id'}))
    pospeech = forms.CharField(required=False,max_length=40,widget=TextDiv(attrs={'size':4,'class':'input-pospeech text-select'}))    
    dict_type = forms.CharField(required=True,widget=DictLogo())
    data = forms.CharField(required=False,widget=TextDiv(attrs={'size':40,'class':'input-webster_def text-select'}))
    selected_sense = forms.CharField(required=True,widget=forms.HiddenInput(attrs={'class':'input-selected_sense'}))
    
class VocabPreferenceForm(forms.ModelForm):

    class Meta:
        model = VocabPreference
        fields = ['show_cutoff', 'diff_cutoff', 'learner_pref', 'webster_pref']
        widgets = {'show_cutoff':forms.TextInput(attrs={'class':'form-control'}),
                    'diff_cutoff':forms.TextInput(attrs={'class':'form-control'}),
                    'learner_pref':Select2Widget(attrs={'class':'form-control'}),
                    'webster_pref':Select2Widget(attrs={'class':'form-control'}),
                    }
        labels = {'show_cutoff':'Difficulty Cut-Off for Displaying Vocabulary',
                    'diff_cutoff':'Difficulty Cut-Off for Auto-Selecting Vocabulary',
                    'learner_pref':'Webster Learner Dictionary',
                    'webster_pref':'Webster Collegiate Dictionary',
                    }
