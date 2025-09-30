from django import template

register = template.Library()

@register.filter
def get_color(dictionary, key):
    return dictionary.get(key, "#ffffff")
