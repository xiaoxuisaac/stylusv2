from .views import StylusRegistrationView
import views
from django.urls import reverse
from django.conf.urls import url, include
from django.views.generic.base import RedirectView
import forms
from django.contrib.auth.views import (
     password_reset,
     password_reset_done,
     password_reset_confirm,
     password_reset_complete,
     password_change,
     password_change_done,
     login,
     logout
 )
 
urlpatterns = [
     url(r'^logout/',logout,{'next_page':'/'},name='logout'),
     url(r'^password/change/done/$', password_change_done,{'template_name':'registration/password_change_done1.html'},
         name='password_change_done'),
     url(r'^password/change/$', password_change,
     {'template_name':'registration/password_change_lean.html','password_change_form':forms.PasswordChangeForm},
         name='password_change'),
     url(r'^password/reset/$', password_reset,{'template_name':'registration/password_reset_form1.html','password_reset_form':forms.PasswordResetForm},
         name='password_reset'),
     url(r'^password/reset/done$', password_reset_done,{'template_name':'registration/password_reset_done1.html'},
         name='password_reset_done'),
     url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', password_reset_confirm,
         {'template_name':'registration/password_reset_confirm1.html'}, name='password_reset_confirm'),
     url(r'^password/reset/complete$', password_reset_complete,{'template_name':'registration/password_reset_complete1.html'},
         name='password_reset_complete'),
     url(r'^login/$', login, {'template_name': 'login.html', 'authentication_form':forms.AuthenticationForm},name='login'),
     url(r'^register/$',
         StylusRegistrationView.as_view(
             form_class=forms.StylusRegistrationForm
         ),
         name='registration_register'
     ),
     url(r'^register/(?P<verification>[A-Z,0-9]*)/$',
         StylusRegistrationView.as_view(
             form_class=forms.StylusRegistrationForm
         ),
         name='registration_register_invitation',
     ),
     url(r'^', include('registration.backends.hmac.urls')),
     url(r'^profile/(?P<load_url>[0-9,_,a-z,A-Z]*)/$',views.profile),
     url(r'^profile/$',views.profile, name='profile'),
     url(r'^vocab_history/$',views.vocab_history, name='vocab_history'),
     url(r'^vocab_history/get',views.get_vocab, name='get_vocab'),
     url(r'^vocab_history/delete',views.delete_vocab, name='delete_vocab'),
     ]