# core/templatetags/gravatar.py

import hashlib
from django import template

register = template.Library()

@register.filter
def gravatar_url(user, size=40):
    """
    Generates a Gravatar URL for the given user.

    :param user: The user object.
    :param size: The size of the Gravatar image.
    :return: URL string for the user's Gravatar.
    """
    try:
        size = int(size)
    except (ValueError, TypeError):
        size = 40  # Default size

    email = getattr(user, 'email', '').lower().strip()
    if user.is_authenticated and email:
        email_hash = hashlib.md5(email.encode('utf-8')).hexdigest()
        return f"https://www.gravatar.com/avatar/{email_hash}?s={size}&d=identicon"
    else:
        # Return a default avatar image if user is not authenticated or has no email
        return f"https://www.gravatar.com/avatar/?s={size}&d=identicon"


