from django.contrib import admin
from models import *

# Register your models here.

class LogDataAdmin(admin.ModelAdmin):
    list_display = ('created_date','ip_addr', 'owner', 'info')
    
admin.site.register(LogData,LogDataAdmin)
    