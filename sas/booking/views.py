from django.utils.translation import ugettext as _
from django.shortcuts import render,redirect
from .forms import NewUserForm
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
      return render(request,'booking/listuser.html',{})
  else:
    form = NewUserForm()
    return render(request, 'booking/newUser.html', {'form_user':form})

def list_user(request):
  users = UserProfile.objects.all()
  return render(request,'booking/listUser.html',{'users':users})
