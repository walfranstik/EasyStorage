from django import template

register = template.Library()


@register.simple_tag
def discount_percentage(original_price, discounted_price):
    if original_price <= discounted_price:
        return ""
    percentage = round(((original_price - discounted_price) / original_price) * 100)
    return "{}% off".format(percentage)
