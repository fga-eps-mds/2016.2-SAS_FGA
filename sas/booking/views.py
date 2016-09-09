from django.utils.translation import ugettext as _
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic.edit import UpdateView
from .forms import NewUserForm
from .models import UserProfile

def index(request):
    return render(request,'booking/index.html',{})

def new_user(request):
    if request.method == "POST":
      form = NewUserForm(request.POST,UserProfile)
      if not(form.is_valid()):
        return render(request, 'booking/newUser.html', {'form_user':form})
      else:
        user_profile = form.save()
        return render(request,'booking/index.html',{})
    else:
      form = NewUserForm()
      return render(request, 'booking/newUser.html', {'form_user':form})

def list_user(request):
    users = UserProfile.objects.all()
    return render(request,'booking/listUser.html',{'users':users})

def edit_user(request,id):
    user = get_object_or_404(UserProfile, id=id)

    if request.method == "POST":
      form = NewUserForm(request.POST,instance=user)
      if not(form.is_valid()):
        return render(request, 'booking/newUser.html', {'form_user':form})
      else:
        user_profile = form.save()
        return render(request,'booking/index.html',{})
    else:
      form = NewUserForm(initial={'name':user.user.first_name,'username':user.user.username,'email':user.user.email}, instance = user)
      return render(request, 'booking/newUser.html', {'form_user':form})