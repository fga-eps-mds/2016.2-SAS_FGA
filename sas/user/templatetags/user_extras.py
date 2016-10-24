from django import template
from user.models import CATEGORY
from django.utils.translation import ugettext as _

register = template.Library()

@register.filter(name='category')
def category(user):
    return _(CATEGORY[int(user.category)][1])

@register.filter(name='type')
def is_admin(user):
    if user.is_admin():
        return _('Admin')
    else:
        return _('Academic User')
