from django.contrib import admin
from .models import *

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','first_name')
 
class AnalyzedVocabVariablesAdmin(admin.ModelAdmin):
    list_display = ('request_id','owner','created_date')
       
admin.site.register(Profile,ProfileAdmin)
admin.site.register(AnalyzedVocabVariables,AnalyzedVocabVariablesAdmin)
