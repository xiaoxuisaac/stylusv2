from django import template

register = template.Library()

def tex(value):
    value = value.replace('&lt;','<').replace('&gt;','>')
    value = value.replace(': as', ': such as')
    value = value.replace('dt> :', 'dt>')
    value = value.replace(' :', '; ')
    value = value.replace('dt>:', 'dt>')
    value = value.replace('<it>', ' \iffalse <it>\\fi ').replace('</it>', ' \iffalse </it>\\fi ')
    return value.replace('_','\_')

def tex_def(value):
    value = value.replace('<dt>', ' \iffalse <dt>\\fi ').replace('</dt>', ' \iffalse </dt>\\fi ')
    value = value.replace('<un>', ' -\iffalse <un>\\fi ').replace('</un>', ' \iffalse </un>\\fi ')
    value = value.replace('<aq>', ' - ').replace('</aq>', ' ')
    value = value.replace('<fw>', ' \iffalse <fw>\\fi ').replace('</fw>', ' \iffalse </fw>\\fi ')
    value = value.replace('<phrase>', ' ').replace('</phrase>', ' ')
    value = value.replace('<d\_link>', ' \iffalse <d\_link>\\fi ').replace('</d\_link>', ' \iffalse </d\_link>\\fi ')    
    value = value.replace('<sx>', ' \\textsc{ ').replace('</sx>', '} ')
    value = value.replace('<sn>', ' \\textbf{ ').replace('</sn>', '.} ')
    value = value.replace('<snp>', ' ').replace('</snp>', ' ')
    value = value.replace('<wsgram>', ' \iffalse <wsgram>').replace('</wsgram>', '</wsgram>\\fi ')
    value = value.replace('<snote>', ' \iffalse <snote>').replace('</snote>', '</snote>\\fi ')
    value = value.replace('<dx>', ' \iffalse <dx>').replace('</dx>', '</dx>\\fi ')
    value = value.replace('<vi>', ' \iffalse <vi>').replace('</vi>', '</vi>\\fi ')
    value = value.replace('<synref>', ' \iffalse <synref>\\fi ').replace('</synref>', ' \iffalse </synref>\\fi ')
    value = value.replace('<ca>', ' \iffalse <ca>\\fi ').replace('</ca>', ' \iffalse </ca>\\fi ')
    return value
    
def tex_pos(value):
    pos_dic = {
        'nounpluralbutsingularorpluralinconstruction':'n.',
        'noun':'n.',
        'verb':'v.',
        'adjective':'adj.',
        'adverb':'adv.',
    }
    try:
        return pos_dic[value]
    except:
        return value

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
        'noun':'n.',
        'verb':'v.',
        'adjective':'adj.',
        'adverb':'adv.',
    }
    for key, val in pos_dic.iteritems():
        value = value.replace(key,val)
    return value

def web_glossary_def(value):
    print value
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
register.filter('tex_def', tex_def)
register.filter('tex_pos', tex_pos)


