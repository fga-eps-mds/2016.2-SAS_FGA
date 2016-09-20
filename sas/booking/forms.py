from django.utils.translation import ugettext as _
from django.forms import ModelForm
from .models import UserProfile,Booking,BookTime,Place
from .models import CATEGORY, SPACES, BUILDINGS, WEEKDAYS
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import date
import copy

class LoginForm(ModelForm):
	email = forms.CharField(
					label=_('Email:'),
					widget=forms.TextInput(attrs={'placeholder': 'example@email.com'}))
	password = forms.CharField(
					label=_('Password:'),
					widget=forms.PasswordInput(attrs={'placeholder': ''}))

	def save(self, force_insert=False, force_update=False, commit=True):
		username = self.cleaned_data.get("email")	
		password = self.cleaned_data.get("password")	
		user = authenticate(username=username, password=password)
		if user is None:
			self.add_error('password', _('Email or Password does not match'))
		return user

	class Meta:
		model = User
		fields = ['email', 'password']

class UserForm(ModelForm):
	name = forms.CharField(
					label=_('Name:'),
					widget=forms.TextInput(attrs={'placeholder': ''}))
	email = forms.CharField(
					label=_('Email:'),
					widget=forms.TextInput(attrs={'placeholder': ''}))
	password = forms.CharField(
					label=_('Password:'),
					required=False,
					widget=forms.PasswordInput(attrs={'placeholder': ''}))
	repeat_password = forms.CharField(
					label=_('Repeat Password:'),
					required=False,
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
		print(commit)
		# do custom stuff
		if commit:
			userprofile.save()
		return userprofile

	class Meta:
		model = UserProfile
		fields = ['name', 'registration_number',
				  'category', 'email', 'password', 'repeat_password']

class EditUserForm(UserForm):
	
	class Meta:
		model = UserProfile
		fields = ['name', 'registration_number',
				  'category', 'email']

class NewUserForm(UserForm):

	def clean(self):
		cleaned_data = super(UserForm, self).clean()
		password1 = cleaned_data.get('password')
		password2 = cleaned_data.get('repeat_password')
		if password1 and password2 and password1 != password2:
			self.add_error('password', _('Passwords do not match'))	


class BookingForm(forms.Form):
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
	week_days = forms.MultipleChoiceField(label=_("Days of week"), choices=WEEKDAYS, widget=forms.CheckboxSelectMultiple())	

	def save(self,user, force_insert=False, force_update=False, commit=True):
		spaces = dict(SPACES)
		booking = Booking()
		booking.user = user
		booking.name = self.cleaned_data.get("name")
		booking.start_date = self.cleaned_data.get("start_date")
		booking.end_date = self.cleaned_data.get("end_date")
		booking.place = Place()
		booking.place.name = spaces[self.cleaned_data.get("place")] 
		weekdays =  self.cleaned_data.get("week_days")
		book = BookTime()
		book.date_booking = booking.start_date
		book.start_hour = self.cleaned_data.get("start_hour")
		book.end_hour = self.cleaned_data.get("end_hour")
		finish_date = False
		booking.save()	
		if booking.exists(book.start_hour,book.end_hour,weekdays):
			booking.delete()
			return None
		else:
			while not finish_date:
				for days in weekdays:
					print(days)
					book.next_week_day(int(days))
					if book.date_booking < booking.end_date:
						newobj = copy.deepcopy(book) 
						newobj.save()
						print("pk book time",newobj.pk)
						booking.time.add(newobj)
					else:
						finish_date = True
						break
			booking.save()
			return booking	
		# do custom stuff
			
	def clean(self):
		cleaned_data = super(BookingForm, self).clean()
		if date.today() > cleaned_data.get('start_date'):
			msg = 'A data de inicio deve ser posterior a data atual.'
			self.add_error('start_date', msg)
			raise forms.ValidationError(msg)
		if date.today() > cleaned_data.get('end_date'):
			msg = 'A data final deve ser posterior a data atual.'
			self.add_error('end_date', msg)
			raise forms.ValidationError(msg)
		elif cleaned_data.get('end_date') < cleaned_data.get('start_date'):
			msg = 'A data final deve ser posterior a data de inicio.'
			self.add_error('end_date', msg)
			raise forms.ValidationError(msg)
		if cleaned_data.get('end_hour') <= cleaned_data.get('start_hour'):
			msg = 'A hora final deve ser posterior a hora inicial.'
			self.add_error('end_hour', msg)
			raise forms.ValidationError(msg)
		if date.today() == cleaned_data.get('start_date') and date.today() == cleaned_data.get('end_date') and datetime.now() > cleaned_data.get('start_hour'):
			msg = 'A hora de inicio deve ser posterior a hora atual para uma reserva hoje'
			self.add_error('start_hour', msg)
			raise forms.ValidationError(msg)
		if date.today() == cleaned_data.get('start_date') and date.today() == cleaned_data.get('end_date') and datetime.now() > cleaned_data.get('end_hour'):
			msg = 'A hora final deve ser posterior a hora atual para uma reserva hoje'
			self.add_error('end_hour', msg)
			raise forms.ValidationError(msg)

	
