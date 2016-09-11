from django.utils.translation import ugettext as _
from django.shortcuts import render,redirect
from .forms import UserForm
from .models import UserProfile
from django.contrib.auth import authenticate ,login, logout

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
        return render(request, 'booking/index.html',{}) # voltar a página de perfil do usuário -> ainda não existe
     else:
        return render(request, 'booking/index.html',{})
