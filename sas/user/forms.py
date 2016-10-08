from django.utils.translation import ugettext as _
from django.forms import ModelForm
from .models import UserProfile
from .models import CATEGORY
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate

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
			self.add_error('password', _('Email or Password does not match'))
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
			self.add_error('password', _('Password is wrong'))
			return False
		return True

	def clean(self):
		cleaned_data = super(ModelForm, self).clean()
		password1 = cleaned_data.get('new_password')
		password2 = cleaned_data.get('renew_password')
		if password1 and password2 and password1 != password2:
			self.add_error('new_password', _('Passwords do not match'))
			self.add_error('renew_password', _('Password	s do not match'))

	class Meta:
		model = User
		fields = ['password', 'new_password', 'renew_password']


class UserForm(ModelForm):
	name = forms.CharField(
		label=_('Name:'),
		widget=forms.TextInput(attrs={'placeholder': ''}))
	email = forms.EmailField(
		label=_('Email:'),
		widget=forms.TextInput(attrs={'placeholder': 'example@email.com'}))
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

	def save(self, force_insert=False, force_update=False, commit=True):
		userprofile = super(UserForm, self).save(commit=False)
		# if it is a new user
		if not hasattr(userprofile, 'user'):
			userprofile.user = User()
			userprofile.user.set_password(self.cleaned_data.get('password'))

		userprofile.name(self.cleaned_data.get('name'))
		userprofile.user.email = self.cleaned_data.get('email')
		userprofile.user.username = userprofile.user.email
		userprofile.user.set_password(self.cleaned_data.get('password'))
		print(commit)
		# do custom stuff
		if commit:
			userprofile.save()
		return userprofile

	def clean(self):
		cleaned_data = super(ModelForm, self).clean()
		if not hasattr(self.instance, 'user') or self.instance.user.email != cleaned_data.get('email'):
			if User.objects.filter(username=cleaned_data.get('email')).exists():
				self.add_error('email', _('Email already used'))
		return cleaned_data

	class Meta:
		model = UserProfile
		fields = ['name', 'registration_number', 'category', 'email',
												'password', 'repeat_password']


class EditUserForm(UserForm):

	class Meta:
		model = UserProfile
		fields = ['name', 'registration_number', 'category', 'email']


class NewUserForm(UserForm):

	def clean(self):
		cleaned_data = super(NewUserForm, self).clean()
		password1 = cleaned_data.get('password')
		password2 = cleaned_data.get('repeat_password')

		if len(password1) < 4 :
			msg = _('Password must have at least four characters.')
			self.add_error('password', msg)
			raise forms.ValidationError(msg)
		if password1 and password2 and password1 != password2:
			self.add_error('password', _('Passwords do not match.'))
