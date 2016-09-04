from django.utils.translation import ugettext as _
from django.shortcuts import render,redirect
from .forms import UserForm
from .models import UserProfile

def index(request):
  return render(request,'booking/index.html',{})

def new_user(request):
  if request.method == "POST":
    form = UserForm(request.POST,UserProfile)
    if not(form.is_valid()):
      return render(request, 'booking/newUser.html', {'form_user':form})
    else:
      user_profile = form.save()
      return render(request,'booking/index.html',{})
  else:
    form = UserForm()
    return render(request, 'booking/newUser.html', {'form_user':form})


