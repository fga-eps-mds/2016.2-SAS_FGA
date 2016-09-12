from django.utils.translation import ugettext as _
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic.edit import UpdateView
from .forms import NewUserForm, EditUserForm
from .models import UserProfile, User

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

def edit_user(request,id=None):
    instance = get_object_or_404(UserProfile, id=id)
    user = instance.user     
    
    form = EditUserForm(request.POST or None,initial={'name':user.first_name,'email':user.email,'password':user.password},instance=user)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return render(request,'booking/index.html',{})

    return render(request, 'booking/editUser.html', {"form_user":form})