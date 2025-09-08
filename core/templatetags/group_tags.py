# core/templatetags/group_tags.py
from django import template

register = template.Library()

@register.filter(name='has_group') 
def has_group(user, group_name):
    """
    Checks if the user belongs to a group with the given name.
    Usage in template: {% if user|has_group:"admin" %}
    """
    return  user.groups.filter(name=group_name).exists()
