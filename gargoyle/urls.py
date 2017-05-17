from django.conf.urls import url, include
from django.views.generic.base import RedirectView
from gargoyle import views
from gargoyle import forms


urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^feedback/', views.feedback, name ='feedback'),
    url(r'^vocab/$', views.vocab, name ='vocab'),
    url(r'^vocab/(?P<prepare>[a-z]*)/$', views.vocab),
    url(r'^progress', views.progress, name ='progress'),
    url(r'^senses/(?P<gid>[0-9]*)/$', views.get_all_defs, name ='senses'),
    url(r'^changedefs/', views.change_defs, name ='change_defs'),
    url(r'^addlemma/(?P<gid>[0-9]*)/$', views.add_lemma, name ='add_lemma'),
    url(r'^pdf/$', views.get_pdf, name ='get_pdf'),    
    url(r'^pdf/(?P<order>[a-z,A-Z]*)/$', views.get_pdf),    
    url(r'^quiz/', views.quiz, name ='quiz'),    
    url(r'^quiz-pdf/', views.quiz_pdf, name ='quiz-pdf'), 
]