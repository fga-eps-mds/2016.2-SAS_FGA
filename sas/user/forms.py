from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm
from .models import UserProfile, Validation
from .models import CATEGORY
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    email = forms.EmailField(
        label=_('Email:'),
        widget=forms.TextInput(attrs={'placeholder': 'example@email.com'}))
    password = forms.CharField(
        label=_('Password:'),
        widget=forms.PasswordInput(attrs={'placeholder': ''}))

    def authenticate_user(self):
        username = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if user is None:
            raise ValidationError({'password': [_('Email or Password does not match'),]})
        return user

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        self.authenticate_user()
        return cleaned_data


class PasswordForm(ModelForm):
    password = forms.CharField(
        label=_('Password:'),
        widget=forms.PasswordInput(attrs={'placeholder': ''}))
    new_password = forms.CharField(
        label=_('New Password:'),
        widget=forms.PasswordInput(attrs={'placeholder': ''}))
    renew_password = forms.CharField(
        label=_('Repeat Password:'),
        widget=forms.PasswordInput(attrs={'placeholder': ''}))

    def save(self, user):
        password = self.cleaned_data.get("new_password")
        user.set_password(password)
        user.save()

    def is_password_valid(self, username):
        cleaned_data = super(ModelForm, self).clean()
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            self.add_error('password', _('Current password is wrong'))

            return False
        return True

    def clean(self):
        cleaned_data = super(ModelForm, self).clean()
        password1 = cleaned_data.get('new_password')
        password2 = cleaned_data.get('renew_password')
        if password1 and password2 and password1 != password2:
            raise ValidationError({'renew_password': [_('Passwords do not match'),]})

    class Meta:
        model = User
        fields = ['password', 'new_password', 'renew_password']


class UserForm(ModelForm):
    name = forms.CharField(
        label=_('Name:'),
        widget=forms.TextInput(attrs={'placeholder': ''}))
    email = forms.EmailField(
        label=_('Email:'),
        widget=forms.TextInput(attrs={'placeholder': 'example@email.com'}),
        error_messages= {'invalid': _('Email address must be in a valid format.')})

    password = forms.CharField(
        label=_('Password:'),
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': ''}))
    repeat_password = forms.CharField(
        label=_('Repeat Password:'),
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': ''}))
    registration_number = forms.CharField(
        label=_('Registration number:'),
        widget=forms.TextInput(attrs={'placeholder': ''}))
    category = forms.ChoiceField(choices=CATEGORY, label=_('Category:'))

    def save(self, force_insert=False, force_update=False, commit=True, is_edit_form=False):
        userprofile = super(UserForm, self).save(commit=False)

        # if it is a new user
        if not hasattr(userprofile, 'user'):
            userprofile.user = User()
            userprofile.user.set_password(self.cleaned_data.get('password'))

        userprofile.name(self.cleaned_data.get('name'))
        userprofile.user.email = self.cleaned_data.get('email')
        userprofile.user.username = userprofile.user.email

        if not is_edit_form:
            userprofile.user.set_password(self.cleaned_data.get('password'))

        # do custom stuff
        if commit:
            userprofile.save()
        return userprofile

    def clean(self):
        cleaned_data = super(ModelForm, self).clean()
        validation = Validation()

        if not hasattr(self.instance, 'user') or self.instance.user.email != cleaned_data.get('email'):
            if User.objects.filter(username=cleaned_data.get('email')).exists():
                raise ValidationError({'email': [_('Email already used'),]})

        # Name validation
        name = cleaned_data.get('name')

        if (len(name) < 2 or len(name) > 50):
            raise ValidationError({'name': [_('Name must be between 2 and 50 characters.'),]})

        if validation.hasSpecialCharacters(name):
            raise ValidationError({'name': [_('Name cannot contain special characters.'),]})

        if validation.hasNumbers(name):
            raise ValidationError({'name': [_('Name cannot contain numbers.'),]})

        return cleaned_data

    class Meta:
        model = UserProfile
        fields = ['name', 'registration_number', 'category', 'email', 'password', 'repeat_password']



class EditUserForm(UserForm):

    class Meta:
        model = UserProfile
        fields = ['name', 'registration_number', 'category', 'email']


class NewUserForm(UserForm):

    def clean(self):
        cleaned_data = super(NewUserForm, self).clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('repeat_password')

        if len(password1) < 6 or len(password1) > 15:
            raise ValidationError({'password': [_('Password must be between 6 and 15 characters.'), ]})

        if password1 and password2 and password1 != password2:
            raise ValidationError({'repeat_password': [_('Passwords do not match.'), ]})
