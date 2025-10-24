from django import template

register = template.Library()

@register.filter
def get_color(dictionary, key):
    color = dictionary.get(key, (1.0, 1.0, 1.0)) 

    if isinstance(color, tuple):
        r, g, b = color
        return f"rgb({int(r*255)}, {int(g*255)}, {int(b*255)})"
    
    return color
