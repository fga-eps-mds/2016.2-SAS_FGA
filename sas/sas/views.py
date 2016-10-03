from django.utils.translation import ugettext as _
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from user.forms import LoginForm


def index(request):
    form = LoginForm()
    return render(request, 'sas/index.html', {'form': form})
