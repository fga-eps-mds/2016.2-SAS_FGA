from django.utils.translation import ugettext as _
from django.shortcuts import render, redirect
from .forms import PasswordForm, SettingsForm
from .forms import NewUserForm, LoginForm, EditUserForm, UserForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib import messages
from sas.views import index
from django.contrib.auth.decorators import login_required
from sas.decorators.decorators import required_to_be_admin
from django.views.generic.edit import FormView
from django.views import View

class NewUserView(FormView):
    template_name = "user/newUser.html"
    form_class = UserForm
    success_url = "/"

    def form_valid(self, form):
        form.insert()
        messages.success(self.request, _('You have been registered'))
        return super(NewUserView, self).form_valid(form)

class EditUserView(View):

    def post(self, request):
        user_form = UserForm(request.POST, editing=True,
                             instance=request.user.profile_user)
        if user_form.is_valid():
            useprofile = user_form.update(request.user.profile_user)
            request.user.refresh_from_db()
            messages.success(request, _('Your data has been updated'))
        return self.get(request,user_form=user_form)

    def get(self, request, user_form=None):
        if user_form is None:
            user_form = UserForm(instance=request.user.profile_user)
        change_form = PasswordForm()
        return render(request,
                      'user/editUser.html',
                      {'form_user': user_form, 'change_form': change_form})


class LoginView(FormView):
    template_name = "user/newUser.html"
    form_class = LoginForm
    success_url = "/"

    def form_valid(self, form):
        user = form.authenticate_user()
        login(self.request, user)
        return super(LoginView, self).form_valid(form)

    def form_invalid(self, form):
        return index(self.request, login_form=form)

    def get(self, request, *args, **kwargs):
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


class ChangePasswordView(FormView):
    form_class = PasswordForm

    def render_template(self, change_form=PasswordForm()):
        user_form = UserForm(instance=self.request.user.profile_user)
        return render(self.request,
                      'user/editUser.html',
                      {'form_user': user_form, 'change_form': change_form})

    def form_valid(self, form):
        if(form.is_password_valid(self.request.user.username)):
            form.save(self.request.user)
            login(self.request, self.request.user)
            messages.success(self.request,
                             _('Your password has been changed'))
            return self.render_template()
        else:
            return self.render_template(change_form=form)

    def form_invalid(self, form):
        return self.render_template(change_form=form)

    def get(self, request, *args, **kwargs):
        return redirect('index')


@login_required(login_url='/?showLoginModal=yes')
@required_to_be_admin
def search_user(request):
    id = request.user.profile_user.id
    users = UserProfile.objects.all().exclude(pk=id)
    return render(request, 'user/searchUser.html', {'users': users})


@login_required(login_url='/?showLoginModal=yes')
@required_to_be_admin
def settings(request):
    if request.method == "POST":
        form = SettingsForm(request.POST)
        if not(form.is_valid()):
            return render(request, 'user/settings.html',
                          {'form_settings': form})
        else:
            form.save()
            messages.success(request, _('Settings updated'))
            return index(request)
    else:
        form = SettingsForm()
        return render(request, 'user/settings.html', {'form_settings': form})


@login_required(login_url='/?showLoginModal=yes')
@required_to_be_admin
def make_user_an_admin(request, id):
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
