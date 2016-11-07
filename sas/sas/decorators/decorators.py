from sas.views import index
from functools import wraps
from django.contrib import messages

def required_to_be_admin(function):
    def wrap(request, *args, **kwargs):
        if hasattr(request.user, 'profile_user') and request.user.profile_user.is_admin():
            return function(request, *args, **kwargs)
        else:
            messages.error(request, 'You cannot access this page.')
            return index(request)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
