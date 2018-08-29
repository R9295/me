from django import template
from django.urls import reverse_lazy

register = template.Library()


@register.simple_tag
def inc_url(id, platform, redir=None):
    if id:
        url = reverse_lazy('analytics:increment', kwargs={
            'user_id':  id,
            'platform': platform
        })
        if redir:
            url = url+'?redir='+redir
        return url
    # incase of preview
    return redir or "#"
