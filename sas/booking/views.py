from django.utils.translation import ugettext as _
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserProfile


def index(request):
    return render(request, 'booking/index.html', {})


def new_user(request):
	if request.method == "POST":
		form = UserForm(request.POST, UserProfile)
		if not(form.is_valid()):
			return render(request, 'booking/newUser.html', {'form_user': form})
		else:
			user_profile = form.save()
			return render(request, 'booking/index.html', {})
	else:
		form = UserForm()
		return render(request, 'booking/newUser.html', {'form_user': form})


def list_user(request):
	users = UserProfile.objects.all()
	return render(request, 'booking/listUser.html', {'users': users})


def edit_user(request):
	if request.user.is_authenticated() and request.method == "POST":
		form = UserForm(request.POST, instance=request.user)
		if not(form.is_valid()):
			form.save()
			return render(request, 'booking/newUser.html', {'form_user': form})
		else:
			return render(request, 'booking/newUser.html', {'form_user': form})
	elif not request.user.is_authenticated():
		return render(request, 'login/login.html', {})
	else:
		print("aqui")
		print(request.user.pk)
		user = request.user
		initial = {}
		initial['name'] = user.profile_user.full_name()
		initial['username'] = user.username
		initial['email'] = user.email
		form = UserForm(initial=initial, instance=request.user.profile_user)
		return render(request, 'booking/newUser.html', {'form_user': form})


def login_user(request):
	if request.method == "POST":
		username = request.POST['Username']
		password = request.POST['Password']
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return render(request, 'booking/myIndex.html', {})
		else:
			return HttpResponse("Email ou senha inválidos.")
	else:
		return render(request, 'booking/index.html', {})


def logout_user(request):
	logout(request)
	return render(request, 'booking/index.html', {})


def delete_user(request):
	if request.user.is_authenticated():
		User.objects.get(pk=request.user.pk).delete()
		return render(request, 'booking/deleteSucceeded.html', {})
	elif request.POST['cancel']:
		return render(request, 'booking/listUser.html', {})
	else:
		return render(request, 'login/login.html', {})

def new_booking(request):
    if request.user.is_authenticated():
        if request.method == "POST":
            form_booking = BookingForm(request.POST, Booking)
            if not(form_booking.is_valid()):
	               return render(request, 'booking/newBooking.html', {'form_booking':form_booking})
            else:
                email = User.objects.get(pk=request.user.pk).email
                booking = form_booking.save()
                return render(request, 'booking/index.html', {})
        else:
            form_booking = BookingForm()
            return render(request, 'booking/newBooking.html', {'form_booking':form_booking})

    else:
    	return render(request, 'booking/index.html', {})
