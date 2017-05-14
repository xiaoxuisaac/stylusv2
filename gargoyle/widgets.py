from django.forms.widgets import Widget
from django.template import loader
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape, format_html, html_safe
from django.forms.utils import flatatt, to_current_timezone
import copy

class TextDiv(Widget):
    template_name = 'widgets/text_div_widget.html'

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        attrs_div = copy.deepcopy(attrs) 
        attrs_div['id']+='-div'
        name_div = name+'-div'
        final_attrs = self.build_attrs(attrs, name=name, value = value)
        final_attrs_div = self.build_attrs(attrs_div, name=name_div)
        return format_html(u'<input{} style="display:none"/>'+u'<div{}> {} </div>', flatatt(final_attrs),flatatt(final_attrs_div),value)
    
        
class DefMenuIcon(Widget):
    template_name = 'widgets/def_menu_icon_widget.html'

    def get_context(self, name, value, attrs=None):
        return {'widget': {
            'name': name,
            'value': value,
            'attrs':attrs
        }}

    def render(self, name, value, attrs=None):
        context = self.get_context(name, value, attrs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)
        
class DictLogo(Widget):
    template_name = 'widgets/dict_logo.html'
    def get_context(self, name, value, attrs=None):
        return {'widget': {
            'name': name,
            'value': value,
            'attrs':attrs
        }}
    def render(self, name, value, attrs=None):
        context = self.get_context(name, value, attrs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)