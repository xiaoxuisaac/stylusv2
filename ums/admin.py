from django.contrib import admin
from .models import *
from django.utils.translation import ugettext_lazy as _

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','first_name')
    actions = ['send_welcome_email']
    
    def send_welcome_email(self, request, queryset):
        from django.core.mail import EmailMultiAlternatives
        from django.template import loader
        for profile in queryset:
            subject = loader.render_to_string('emails/welcome_email_subject.txt', {'profile':profile})
            subject = ''.join(subject.splitlines())
            body = loader.render_to_string('emails/welcome_email.txt', {'profile':profile})
            email_message = EmailMultiAlternatives(subject, body, None, [profile.user.email])
            email_message.send()
    send_welcome_email.short_description=_(u'send welcome back email to selected user profile')
    
class AnalyzedVocabVariablesAdmin(admin.ModelAdmin):
    list_display = ('request_id','owner','created_date')
       
admin.site.register(Profile,ProfileAdmin)
admin.site.register(AnalyzedVocabVariables,AnalyzedVocabVariablesAdmin)
