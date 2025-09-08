# grants/templatetags/table_extras.py
from django import template

register = template.Library()


@register.simple_tag
def my_table_page_url(table, page_number):
    """
    Returns the correct pagination URL for a given table and page number.
    """
    return table.page_url(page_number)
