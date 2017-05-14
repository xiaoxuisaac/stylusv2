from django.contrib import admin
from .models import *
from django.utils.translation import ugettext_lazy as _


# Register your models here.

class OcrBundleAdmin(admin.ModelAdmin):
    actions = ['duplicate']
    list_display = ('user','name','remains','repeat_remain','expired')
    search_fields = ('user__user__username', 'user__first_name', 'user__last_name')
    def duplicate(self, request, queryset):
        for ocrbundle in queryset:
            ocrbundle.copy()
        return
    duplicate.short_description=_(u'duplicate this ocr bundle')
class OcrBundleModelAdmin(admin.ModelAdmin):
    list_display = ('name','initial_value','expiration_date','repeat','code')

class OcrFileAdmin(admin.ModelAdmin):
    list_display = ('upload','owner','saved_date')  
      

admin.site.register(OcrFile,OcrFileAdmin)
admin.site.register(OcrBundle,OcrBundleAdmin)
admin.site.register(OcrBundleModel,OcrBundleModelAdmin)