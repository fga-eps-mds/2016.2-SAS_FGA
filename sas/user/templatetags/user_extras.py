from django import template

register = template.Library()

@register.filter(name='is_admin')
def is_admin(user):
    if hasattr(user,"profile_user"):
        return user.profile_user.is_admin()
    else:
        return False
