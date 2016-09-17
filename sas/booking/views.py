from django.utils.translation import ugettext as _
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm, NewUserForm, LoginForm, EditUserForm
from .forms import PasswordForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserProfile


def index(request):
	form = LoginForm()
	return render(request, 'booking/index.html', {'form':form})

def index_user(request):
    return render(request, 'booking/myIndex.html', {})

def new_user(request):
	if request.method == "POST":
		form = NewUserForm(request.POST, UserProfile)
		if not(form.is_valid()):
			return render(request, 'booking/newUser.html', {'form_user': form})
		else:
			user_profile = form.save()
			form = LoginForm()
			return render(request, 'booking/index.html', {'form':form})
	else:
		form = NewUserForm()
		return render(request, 'booking/newUser.html', {'form_user': form})


def list_user(request):
    users = UserProfile.objects.all()
    return render(request, 'booking/listUser.html', {'users': users})


def edit_user(request):
	if request.user.is_authenticated() and request.method == "POST":
		form = EditUserForm(request.POST, instance=request.user.profile_user)
		if form.is_valid():
			user = form.save()
		return render_edit_user(request,user_form=form)	
	elif not request.user.is_authenticated():
		return index(request) 
	else:
		return render_edit_user(request)	

def render_edit_user(request,user_form=None,change_form=PasswordForm()):
	user = request.user
	initial = {}
	initial['name'] = user.profile_user.full_name()
	initial['email'] = user.email
	if user_form is None:
		user_form = EditUserForm(initial=initial, 
								 instance=request.user.profile_user)
	return render(request, 
				  'booking/editUser.html', 
				  {'form_user': user_form,'change_form':change_form})

def login_user(request) :
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			user = form.save()
			if user is not None:
				login ( request , user) ;
				return render (request ,'booking/myIndex.html',{})
			else:
				return render (request,'booking/index.html',{'form':form})
	else:
		return index(request) 

def logout_user(request):
	logout(request)
	form = LoginForm()
	return render(request, 'booking/index.html', {'form': form})


def delete_user(request):
    if request.user.is_authenticated():
        User.objects.get(pk=request.user.pk).delete()
        form = LoginForm()
        return render(request, 'booking/index.html', {'form': form})
    else:
        return render(request, 'booking/editUser.html', {})

def change_password(request):
	if request.user.is_authenticated() and request.POST:
		form = PasswordForm(request.POST)
		if form.is_valid() and form.is_password_valid(request.user.username):
			form.save(request.user)
			login(request,request.user)
			return render_edit_user(request)
		else:
			return render_edit_user(request,change_form=form)		
	if not request.user.is_authenticated():
		return index(request)
	else:
		return render_edit_user(request)	
		
