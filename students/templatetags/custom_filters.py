from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    """
    Template filter to access dictionary items with variable keys.
    Usage: {{ my_dict|get_item:my_key }}
    """
    if dictionary is None:
        return None
    
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    
    try:
        return getattr(dictionary, key)
    except (AttributeError, TypeError):
        return None 