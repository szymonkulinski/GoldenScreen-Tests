import json
from django import template
from repertoire.models import Hall

register = template.Library()

@register.simple_tag
def saved_halls(_name):
    return Hall.objects.filter(name=_name)[0]
