from django import template
from django.utils import timezone, dateparse
from django.template.defaulttags import register

from Management.models import *

register = template.Library()

@register.filter(name='access')
def access(value, arg):
    return value[arg]
