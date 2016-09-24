from django.utils.translation import ugettext as _
from django.forms import ModelForm
from .models import UserProfile, Booking, BookTime, Place
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
			self.add_error('renew_password', _('Passwords do not match'))

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


class BookingForm(forms.Form):
	name = forms.CharField(
		label=_('Booking Name:'),
		widget=forms.TextInput(attrs={'placeholder': ''}))
	start_hour = forms.TimeField(
		label=_('Start Time:'),
		widget=forms.widgets.TimeInput(attrs={'placeholder': ''}))
	end_hour = forms.TimeField(
		label=_('End Time:'),
		widget=forms.widgets.TimeInput(attrs={'placeholder': ''}))
	start_date = forms.DateField(
		label=_('Start Date:'),
		widget=forms.widgets.DateInput(attrs={'placeholder': ''}))
	end_date = forms.DateField(
		label=_('End Date:'),
		widget=forms.widgets.DateInput(attrs={'placeholder': ''}))
	place = forms.ChoiceField(choices=SPACES, label=_('Place:'))
	building = forms.ChoiceField(choices=BUILDINGS, label=_('Building:'))
	week_days = forms.MultipleChoiceField(label=_("Days of week: "),
						choices=WEEKDAYS, widget=forms.CheckboxSelectMultiple())

	def save(self, user, force_insert=False, force_update=False, commit=True):
		spaces = dict(SPACES)
		booking = Booking()
		booking.user = user
		booking.name = self.cleaned_data.get("name")
		booking.start_date = self.cleaned_data.get("start_date")
		booking.end_date = self.cleaned_data.get("end_date")
		booking.place = Place()
		booking.place.name = spaces[self.cleaned_data.get("place")]
		weekdays = self.cleaned_data.get("week_days")
		book = BookTime()
		book.date_booking = booking.start_date
		book.start_hour = self.cleaned_data.get("start_hour")
		book.end_hour = self.cleaned_data.get("end_hour")
		finish_date = False
		booking.save()
		if booking.exists(book.start_hour, book.end_hour, weekdays):
			booking.delete()
			return None
		else:
			while not finish_date:
				for days in weekdays:
					book.next_week_day(int(days))
					if book.date_booking < booking.end_date:
						newobj = copy.deepcopy(book)
						newobj.save()
						print("pk book time", newobj.pk)
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
			msg = _('Start date must be after current date.')
			self.add_error('start_date', msg)
			raise forms.ValidationError(msg)
		if date.today() > cleaned_data.get('end_date'):
			msg = _('End date must be after current date.')
			self.add_error('end_date', msg)
			raise forms.ValidationError(msg)
		elif cleaned_data.get('end_date') < cleaned_data.get('start_date'):
			msg = _('End date must be after start date.')
			self.add_error('end_date', msg)
			raise forms.ValidationError(msg)
		if cleaned_data.get('end_hour') <= cleaned_data.get('start_hour'):
			msg = _('End hour must occur after start hour.')
			self.add_error('end_hour', msg)
			raise forms.ValidationError(msg)
		if date.today() == cleaned_data.get('start_date') and date.today() == cleaned_data.get('end_date') and datetime.now() > cleaned_data.get('start_hour'):
			msg = ('Start hour must occur after current hour for a booking today')
			self.add_error('start_hour', msg)
			raise forms.ValidationError(msg)
		if date.today() == cleaned_data.get('start_date') and date.today() == cleaned_data.get('end_date') and datetime.now() > cleaned_data.get('end_hour'):
			msg = _('End hour must occur after current hour for a booking today')
			self.add_error('end_hour', msg)
			raise forms.ValidationError(msg)
