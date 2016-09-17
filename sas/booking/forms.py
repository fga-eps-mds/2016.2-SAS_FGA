from django.utils.translation import ugettext as _
from django.forms import ModelForm
from .models import UserProfile,Booking,BookTime
from .models import CATEGORY
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.utils import timezone
import datetime

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


	def clean(self):
		cleaned_data = super(UserForm, self).clean()
		if cleaned_data.get('password') != cleaned_data.get('repeat_password'):
			self.add_error('password', 'Senhas nao conferem.')

	class Meta:
		model = UserProfile
		fields = ['name', 'registration_number',
				  'category', 'email', 'password', 'repeat_password']

class BookingForm(ModelForm):
	name = forms.CharField(
					label=_('Nome:'),
					widget=forms.TextInput(attrs={'placeholder': ''}))
	start_hour = forms.TimeField(
					label=_('Hora inicial:'),
					widget=forms.widgets.TimeInput)
	end_hour = forms.TimeField(
					label=_('Hora final:'),
					widget=forms.widgets.TimeInput)
	start_date = forms.DateField(
					label=_('Data inicial:'),
					widget=forms.widgets.DateInput)
	end_date = forms.DateField(
					label=_('Data final:'),
					widget=forms.widgets.DateInput)
	place = forms.CharField(
					label=_('Sala:'),
					widget=forms.TextInput(attrs={'placeholder': ''}))

	def save(self, force_insert=False, force_update=False, commit=True):
		booking = super(BookingForm, self).save(commit=False)
		booking.time = BookTime()
		booking.time.start_hour = self.cleaned_data.get('start_hour')
		booking.time.end_hour = self.cleaned_data.get('end_hour')
		booking.time.start_date = self.cleaned_data.get('start_date')
		booking.time.end_date = self.cleaned_data.get('end_date')

		booking.name = self.cleaned_data.get('name')
		booking.place = self.cleaned_data.get('place')

		# do custom stuff
		if commit:
			booking.save()
		return booking

	def clean(self):
		cleaned_data = super(BookingForm, self).clean()
		if datetime.now() >= cleaned_data.get('start_date'):
			msg = 'A data de inicio deve ser posterior a data atual'
			self.add_error('start_date', msg)
			raise forms.ValidationError(msg)
		if datetime.now() >= cleaned_data.get('end_date'):
			msg = 'A data final deve ser posterior a data atual'
			self.add_error('end_date', msg)
			raise forms.ValidationError(msg)
		elif cleaned_data.get('end_date') < cleaned_data.get('start_date'):
			msg = 'A data final deve ser posterior a data de inicio'
			self.add_error('end_date', msg)
			raise forms.ValidationError(msg)
		if cleaned_data.get('start_date') == cleaned_data.get('end_date') and cleaned_data.get('end_hour') < cleaned_data.get('start_hour'):
			msg = 'A hora final deve ser anterior a hora inicial'
			self.add_error('end_hour', msg)
			raise forms.ValidationError(msg)

	class Meta:
		model = Booking
		fields = ['name', 'place',
				  'start_hour', 'end_hour', 'start_date', 'end_date', 'user']
