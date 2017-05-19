from registration.forms import RegistrationForm as RegistrationBaseForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from .models import *
from django import forms
from django.contrib.auth.forms import PasswordChangeForm as PasswordChangeBaseForm
from django.contrib.auth.forms import AuthenticationForm as AuthenticationBaseForm
from django.contrib.auth.forms import PasswordResetForm as PasswordResetBaseForm

class StylusRegistrationForm(RegistrationBaseForm):
    class Meta(RegistrationBaseForm.Meta):
        fields = [
            User.USERNAME_FIELD,
            'email',
            'password1',
            'password2',
        ]
        widgets = {
                'username' : forms.TextInput(attrs={'class':'form-control'}),
                'email' : forms.EmailInput(attrs={'class':'form-control'})
                }
    password1 = forms.CharField(label=_("Password"),
                    widget=forms.PasswordInput(attrs={'type':'password','class':'form-control'}))
    password2 = forms.CharField(label=_("Password"),
                    widget=forms.PasswordInput(attrs={'type':'password','class':'form-control'}))
    email = forms.CharField(label=_("Email"),
                    widget=forms.EmailInput(attrs={'type':'email','class':'form-control'}))
    invitation = forms.CharField(required=False,
         label='Invitation Code',
         widget=forms.TextInput(attrs={'class':'form-control','placeholder':'type NEW_STYLUS to get 50 pages free for PDF processing.'}))
    def __init__(self, verification=None, *args, **kwargs):
         super(StylusRegistrationForm, self).__init__(*args, **kwargs)
         self.fields['invitation'].initial=verification
    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError(u'This email address has been registered. Try another one')
        return email

class PasswordChangeForm(PasswordChangeBaseForm):
    old_password = forms.CharField(label=_("Old Password"),
                    widget=forms.PasswordInput(attrs={'type':'password','class':'form-control'}))
    new_password1 = forms.CharField(label=_("Password"),
                    widget=forms.PasswordInput(attrs={'type':'password','class':'form-control'}))
    new_password2 = forms.CharField(label=_("Password Confirmation"),
                    widget=forms.PasswordInput(attrs={'type':'password','class':'form-control'}))

class AuthenticationForm(AuthenticationBaseForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'class':'form-control'}))
    
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'type':'password','class':'form-control'})
    )

class PasswordResetForm(PasswordResetBaseForm):
    email = forms.EmailField(label=_("Email"), max_length=254,widget=forms.EmailInput(attrs={'type':'email','class':'form-control'}))
    
