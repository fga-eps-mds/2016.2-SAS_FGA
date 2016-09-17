from django.utils.translation import ugettext as _
from django.forms import ModelForm
from .models import UserProfile,Booking,BookTime
from .models import CATEGORY, SPACES, BUILDINGS
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
					label=_('Nome para Reserva:'),
					widget=forms.TextInput(attrs={'placeholder': ''}))
	start_hour = forms.TimeField(
					label=_('Hora Inicial:'),
					widget=forms.widgets.TimeInput(attrs={'placeholder': ''}))
	end_hour = forms.TimeField(
					label=_('Hora Final:'),
					widget=forms.widgets.TimeInput(attrs={'placeholder': ''}))
	start_date = forms.DateField(
					label=_('Data Inicial:'),
					widget=forms.widgets.DateInput(attrs={'placeholder': ''}))
	end_date = forms.DateField(
					label=_('Data Final:'),
					widget=forms.widgets.DateInput(attrs={'placeholder': ''}))
	place = forms.ChoiceField(choices=SPACES, label=_('Espaço:'))
	building = forms.ChoiceField(choices=BUILDINGS, label=_('Prédio:'))

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

	class Meta:
		model = Booking
		fields = ['name', 'building', 'place', 'start_date', 'end_date', 'start_hour', 'end_hour']
