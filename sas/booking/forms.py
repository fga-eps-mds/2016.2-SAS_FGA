from django.utils.translation import ugettext as _
from django.forms import ModelForm
from .models import UserProfile
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

class UserForm(ModelForm):
	name = forms.CharField(label = _('Name'))
	username = forms.CharField(label = _('Username'))
	email = forms.CharField(label = _('Email'))
	password = forms.CharField(label = _('Password'), widget = forms.PasswordInput())
	repeat_password = forms.CharField(label = _('Repeat Password'), widget = forms.PasswordInput())

	def save(self, force_insert=False, force_update=False, commit=True):
		userprofile = super(UserForm, self).save(commit=False)
		userprofile.user = User()
		userprofile.name(self.cleaned_data.get('name'))
		userprofile.user.email = self.cleaned_data.get('email')
		userprofile.user.username = self.cleaned_data.get('username')
		userprofile.user.set_password(self.cleaned_data.get('password'))

    # do custom stuff
		if commit:
			userprofile.save()
		return userprofile


	def clean(self):
		cleaned_data = super(UserForm,self).clean()
		if cleaned_data.get('password') != cleaned_data.get('repeat_password'):
			self.add_error('password','Senhas nao conferem.')
	
	class Meta:
		model = UserProfile
		exclude = ['user']

