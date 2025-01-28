from django import template
import json
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def json_encode(value):
    return mark_safe(json.dumps(value))