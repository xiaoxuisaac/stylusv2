from django.contrib import admin
from .models import *

# Register your models here.

 
class VocabVariablesAdmin(admin.ModelAdmin):
    list_display = ('request_id','owner','created_date')
       
admin.site.register(VocabVariables,VocabVariablesAdmin)
