"""
A template tag for mojombo/github's clippy.swf, as forked by adamcooke
http://github.com/adamcooke/clippy
"""
from django import template

register = template.Library()

@register.inclusion_tag('clippy/clippy.html', takes_context=True)
def clippy(context, text, bgcolor):
    return {'MEDIA_URL': context['MEDIA_URL'],
            'text': text,
            'bgcolor': bgcolor}

