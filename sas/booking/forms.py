from django.utils.translation import ugettext as _
from django.forms import ModelForm
from .models import UserProfile
from .models import CATEGORY
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password



class UserForm(ModelForm):
	name = forms.CharField(
					label=_('Name:'),
					widget=forms.TextInput(attrs={'placeholder': ''}))
	email = forms.CharField(
					label=_('Email:'),
					widget=forms.TextInput(attrs={'placeholder': ''}))
	password = forms.CharField(
					label=_('Password:'),
					widget=forms.PasswordInput(attrs={'placeholder': ''}))
	repeat_password = forms.CharField(
					label=_('Repeat Password:'),
					widget=forms.PasswordInput(attrs={'placeholder': ''}))
	registration_number = forms.CharField(
					label=_('Registration number:'),
					widget=forms.TextInput(attrs={'placeholder': ''}))
	category = forms.ChoiceField(choices=CATEGORY, label=_('Category:'))

	def save(self, force_insert=False, force_update=False, commit=True):
		userprofile = super(UserForm, self).save(commit=False)
		userprofile.user = User()
		userprofile.name(self.cleaned_data.get('name'))
		userprofile.user.email = self.cleaned_data.get('email')
		userprofile.user.username=userprofile.user.email
		userprofile.user.set_password(self.cleaned_data.get('password'))

		# do custom stuff
		if commit:
			userprofile.save()
		return userprofile

	class Meta:
		model = UserProfile
		fields = ['name', 'registration_number',
				  'category', 'email', 'password', 'repeat_password']

class NewUserForm(UserForm):

	def clean(self):
		cleaned_data = super(UserForm, self).clean()
		password1 = cleaned_data.get('password')
		password2 = cleaned_data.get('repeat_password')
		if password1 and password2 and password1 != password2:
			self.add_error('password', _('Passwords do not match'))	
