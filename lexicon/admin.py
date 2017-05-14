from django.contrib import admin
from .models import *
from django.utils.translation import ugettext_lazy as _

class UndefinedWordPointerAdmin(admin.ModelAdmin):
    actions = ['update']
    list_display = ('word','undefined')
    def update(self, request, queryset):
        for undef in queryset:
            undef.update(forced = queryset.count()==1)
        return
    update.short_description=_(u'update selected undefined words')
# Register your models here.

admin.site.register(UndefinedWordPointer,UndefinedWordPointerAdmin)
