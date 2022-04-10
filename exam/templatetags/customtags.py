from django import template

register = template.Library()

@register.filter()
def total_func(value, value2):
    """Result of Questions"""
    print((value*4)-value2)
    return (value*4)-(value2)

def unatt(v1, v2, v3):
    return v1-v2+v3