from django import template

register = template.Library()

@register.filter
def dict_data(dictionary, dict_key):
    if type(dictionary) == dict:
        try:
            return dictionary[dict_key]
        except KeyError:
            return ''
    else:
        return ''
