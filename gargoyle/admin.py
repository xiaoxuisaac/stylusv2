from django.contrib import admin
from .models import *

# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    list_display = ('day','name')

class TempFileAdmin(admin.ModelAdmin):
    list_display = ('upload','owner','saved_date')  

class SessionVariablesAdmin(admin.ModelAdmin):
    list_display = ('request_id','saved_date','owner')  

admin.site.register(Comment,CommentAdmin)
admin.site.register(TempFile,TempFileAdmin)
admin.site.register(SessionVariables,SessionVariablesAdmin)

