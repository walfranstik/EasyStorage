from django import template
from almacen.models import GeneralSetting


register = template.Library()

@register.simple_tag
def general_setting():
    S=GeneralSetting.objects.first()
    return S
