from django.conf.urls import url, include
from django.views.generic.base import RedirectView
import views

urlpatterns = [
    url(r'^log$', views.log_compound, name='log_compound'),
]