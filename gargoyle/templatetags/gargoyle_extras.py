from django import template

register = template.Library()

def tex(value):
    return value.replace('_','\_')

def web_def(field):
    value = field.as_widget()
    value = value.replace('&lt;','<').replace('&gt;','>')
    value = value.replace(': as', ': such as')
    value = value.replace('dt> :', 'dt>')
    value = value.replace(' :', '; ')
    value = value.replace('dt>:', 'dt>')
    return value
    
def web_pos(field):
    if isinstance(field, str) or isinstance(field, unicode):
        value =field 
    else:
        value = field.as_widget()
    pos_dic = {
        'nounpluralbutsingularorpluralinconstruction':'n.',
        'n.pluralbutsingularorpluralinconstruction':'n.',
        'nounsingularbutsingularorpluralinconstruction':'n.',
        'n.singularbutsingularorpluralinconstruction':'n.',
        'noun':'n.',
        'verb':'v.',
        'adjective':'adj.',
        'adverb':'adv.',
    }
    for key, val in pos_dic.iteritems():
        value = value.replace(key,val)
    return value

def web_glossary_def(value):
    value = value.replace('&lt;','<').replace('&gt;','>')
    value = value.replace(': as', ': such as')
    value = value.replace('dt>:', 'dt>')
    value = value.replace('dt> :', 'dt>')
    value = value.replace(' :', '; ')
    value = value.replace('*', '')
    groups = value.split('</dt>')
    if len(groups)> 6:
        groups = '</dt>'.join(groups[:4]), '</dt>'.join(groups[4:])
        groups = '</dt><span class = "glossary-dt-overflow">'.join(groups)
        groups = groups.split('</dt>')
        groups = '</dt>'.join(groups[:-1]), '</dt>'.join(groups[-1:])
        groups = '</dt></span><a class="glossary-overflow-all" >all &#187;</a><a class="glossary-overflow-collaspe" style="display:none" >collaspe &#171;</a>'.join(groups)
        value = groups
    return value
    
def web_glossary_checkbox(value):
    value = value.replace('&lt;','<').replace('&gt;','>')
    radio = '<label><input class="glossary-dt-selection" type="checkbox"></label>'
    sense_id = '<input class="glossary-sense_id" type="hidden" value="-1">'
    value = value.replace('<dt>', '<dt>'+sense_id+radio)
    return value
    
register.filter('tex', tex)
register.filter('web_def', web_def)
register.filter('web_pos', web_pos)
register.filter('web_glossary_def', web_glossary_def)
register.filter('web_glossary_checkbox', web_glossary_checkbox)

