from django import template

register = template.Library()

@register.filter(name='lookup')
def lookup(value, arg):  # value is obj, arg is attr
    try:
        return getattr(value, arg)
    except AttributeError:
        return ''  # Or handle the error as you see fit
