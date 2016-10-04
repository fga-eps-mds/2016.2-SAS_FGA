from django.utils.translation import ugettext as _
from django.forms import ModelForm
from .models import Booking, BookTime, Place
from .models import SPACES, BUILDINGS, WEEKDAYS
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import date
import copy

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
