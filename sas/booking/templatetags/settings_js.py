from django.utils.safestring import mark_safe
from django.template import Library
import json

register = Library()


@register.filter(is_safe=True)
def js_date(obj):
	return str(obj)
