from django.utils.translation import ugettext as _
from django.shortcuts import render, redirect
from .forms import PasswordForm
from .forms import NewUserForm, LoginForm, EditUserForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib import messages
from sas.views import index
from django.contrib.auth.decorators import login_required


def new_user(request):
    if request.method == "POST":
        form = NewUserForm(request.POST, UserProfile)
        if not(form.is_valid()):
            return render(request, 'user/newUser.html', {'form_user': form})
        else:
            form.save()
            messages.success(request, _('You have been registered'))
            return index(request)
    else:
        form = NewUserForm()
        return render(request, 'user/newUser.html', {'form_user': form})


def list_user(request):
    users = UserProfile.objects.all()
    return render(request, 'user/listUser.html', {'users': users})


def edit_user(request):
    if request.user.is_authenticated() and request.method == "POST":
        form = EditUserForm(request.POST, instance=request.user.profile_user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Your data has been updated'))
        return render_edit_user(request, user_form=form)
    elif not request.user.is_authenticated():
        return index(request)
    else:
        return render_edit_user(request)


def render_edit_user(request, user_form=None, change_form=PasswordForm()):
    user = request.user
    initial = {}
    initial['name'] = user.profile_user.full_name()
    initial['email'] = user.email

    if user_form is None:
        user_form = EditUserForm(initial=initial,
                                 instance=request.user.profile_user)
    return render(request,
                  'user/editUser.html',
                  {'form_user': user_form, 'change_form': change_form})


def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.authenticate_user()
            login(request, user)
            return redirect('index')
        else:
            return index(request, login_form=form)
    else:
        return redirect('index')


def logout_user(request):
    if hasattr(request, 'user') and isinstance(request.user, User):
        logout(request)
        messages.success(request, _('You have been logged out successfully!'))
    return redirect('index')


def delete_user(request):
    if request.user.is_authenticated():
        request.user.delete()
        logout(request)
        return index(request)
    else:
        return index(request)


def change_password(request):
    if request.user.is_authenticated() and request.POST:
        form = PasswordForm(request.POST)
        if form.is_valid() and form.is_password_valid(request.user.username):
            form.save(request.user)
            login(request, request.user)
            messages.success(request, _('Your password has been changed'))
            return render_edit_user(request)
        else:
            return render_edit_user(request, change_form=form)
    if not request.user.is_authenticated():
        return index(request)
    else:
        return render_edit_user(request)


@login_required(login_url='/?showLoginModal=yes')
def search_user(request):
    if request.user.profile_user.is_admin():
        id = request.user.profile_user.id
        users = UserProfile.objects.all().exclude(pk=id)
        return render(request, 'user/searchUser.html', {'users': users})
    else:
        messages.error(request, _('You cannot access this page.'))
        return index(request)


@login_required(login_url='/?showLoginModal=yes')
def make_user_an_admin(request, id):
    if request.user.profile_user.is_admin():
        try:
            user = UserProfile.objects.get(pk=id)
            if user.is_academic_staff():
                user.user.groups.clear()
                user.make_as_admin()
                messages.success(request, _('User ' + user.full_name() +
                                            ' is now an admin.'))
            else:
                messages.error(request, _('User ' + user.full_name() +
                                          ' is already an admin.'))
        except:
            messages.error(request, _('User not found.'))
        finally:
            return search_user(request)
    else:
        messages.error(request, _('You cannot access this page.'))
        return index(request)
