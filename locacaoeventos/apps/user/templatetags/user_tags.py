from django import template

import datetime

register = template.Library()



@register.simple_tag
def photo_from_fb(photo_url): # Only one argument.
    print(photo_url)
    print(photo_url)
    print(photo_url)
    print(photo_url)
    if "http://graph.facebook.com/" in photo_url:
        return True
    else:
        return False