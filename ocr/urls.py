from django.conf.urls import url, include
from django.views.generic.base import RedirectView, TemplateView

from ocr import views


urlpatterns = [
    url(r'^$', views.analyze_to_json, name='analyze_to_json'),
    url(r'^buy/$', TemplateView.as_view(template_name='get_ocr_lean.html'),name='get_ocr')
]