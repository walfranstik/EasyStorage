from django import template
register = template.Library()

@register.filter(name='string_to_int')
def string_to_int(value):
    return int(value)
