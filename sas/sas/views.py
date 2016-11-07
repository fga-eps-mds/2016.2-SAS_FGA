from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from user.forms import LoginForm


def index(request, login_form = LoginForm()):
    if hasattr(request, 'user') and request.user.is_authenticated():
        return render(request, 'sas/home.html', {})
    else:
        return render(request, 'sas/index.html', {'form' : login_form})
