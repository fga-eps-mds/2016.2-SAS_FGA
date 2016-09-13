from django.utils.translation import ugettext as _
from django.shortcuts import render,redirect,get_object_or_404
from .forms import UserForm
from .models import UserProfile
from django.contrib.auth import authenticate ,login, logout
from django.views.generic.edit import UpdateView
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

def login_user ( request) :
    if request.method == "POST":
        username = request.POST[ 'Username'] ;
        password = request.POST[ 'Password'] ;
        user = authenticate ( username=username ,password=password)
        if user is not None:
            login ( request , user) ;
            return render (request ,'login/index.html',{})
        else:
            return render (request ,'login/login.html',{})
    else:
        return render (request ,'login/login.html',{})

def logout_user(request):
   logout(request)
   return render(request,'logout/index.html',{})

def delete_user(request, id):
     if request.POST['delete']:
         User.objects.get(pk = id).delete()
         return render(request, 'booking/deleteSucceeded.html', {})
     elif request.POST['cancel']:
        return render(request, 'booking/listUser.html',{}) 
     else:
        return render(request, 'booking/listUser.html',{})

