from django import template
register = template.Library()

@register.filter(name='multipli')
def multipli(value,arg):
    val=float(value)
    args=float(arg)
    return val*args