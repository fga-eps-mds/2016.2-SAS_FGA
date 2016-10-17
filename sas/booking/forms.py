from django.utils.translation import ugettext_lazy as _
from booking.models import (WEEKDAYS, Booking, BookTime, Place, Building,
							date_range)
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from datetime import date, datetime, timedelta
from django.conf import settings
from django.utils import formats
import copy
import traceback


class BookingForm(forms.Form):
	name = forms.CharField(
		label=_('Booking Name:'),
		widget=forms.TextInput(attrs={'placeholder': ''}))
	start_hour = forms.TimeField(
		label=_('Start Time:'),
		widget=forms.widgets.TimeInput(attrs={'placeholder': '__:__'}))
	end_hour = forms.TimeField(
		label=_('End Time:'),
		widget=forms.widgets.TimeInput(attrs={'placeholder': '__:__'}))
	start_date = forms.DateField(
		label=_('Start Date:'),
		widget=forms.widgets.DateInput(attrs={'placeholder': _("mm/dd/yyyy")}))
	end_date = forms.DateField(
		label=_('End Date:'),
		widget=forms.widgets.DateInput(attrs={'placeholder': _("mm/dd/yyyy")}))
	building = forms.ModelChoiceField(
		queryset=Building.objects,
		label=_('Building:'))
	place = forms.ModelChoiceField(queryset=Place.objects, label=_('Place:'))
	week_days = forms.MultipleChoiceField(label=_("Days of week: "),
						required=False, choices=WEEKDAYS,
						widget=forms.CheckboxSelectMultiple())

	def save(self, user, force_insert=False, force_update=False, commit=True):
		booking = Booking()
		booking.user = user
		booking.name = self.cleaned_data.get("name")
		booking.start_date = self.cleaned_data.get("start_date")
		booking.end_date = self.cleaned_data.get("end_date")
		booking.place = self.cleaned_data.get("place")
		weekdays = self.cleaned_data.get("week_days")

		book = BookTime()
		book.date_booking = booking.start_date
		book.start_hour = self.cleaned_data.get("start_hour")
		book.end_hour = self.cleaned_data.get("end_hour")
		try:
			booking.save()
			if booking.exists(book.start_hour, book.end_hour, weekdays):
				return None
			else:
				for day in date_range(book.date_booking, booking.end_date):
					if(day.isoweekday()-1 in map(int, weekdays)):
						newBookTime = BookTime(start_hour=book.start_hour,
										end_hour=book.end_hour,
										date_booking=day)
						newBookTime.save()
						booking.time.add(newBookTime)
				booking.save()
		except Exception as e:
			booking.delete()
			msg = _('Failed to book selected period')
			print(e)
			raise forms.ValidationError(msg)
			return None
		return booking

	def clean_week_days(self):
		weekdays = self.cleaned_data['week_days']
		try:
			start_date = self.cleaned_data['start_date']
			end_date = self.cleaned_data['end_date']
			if( (end_date-start_date).days > 7 and
					not weekdays):#7 days in a week
				msg = _('Select a repeating standard for the date interval')
				self.add_error('week_days', msg)
			elif not weekdays:
				period = date_range(start_date, end_date)
				for day in period:
					weekdays.append(day.weekday())
		except:
			msg = _('Period invalid')
			raise forms.ValidationError(msg)
		return weekdays

	def clean(self):
		try:
			cleaned_data = super(BookingForm, self).clean()
			today = date.today()
			now = datetime.now()
			start_date = self.cleaned_data['start_date']
			end_date = self.cleaned_data['end_date']
			start_hour = cleaned_data.get('start_hour')
			end_hour = cleaned_data.get('end_hour')
			if not (today <= start_date <= end_date):
				msg = _('Invalid booking period: Booking must be'
						' in future dates')
				self.add_error('start_date', msg)
				self.add_error('end_date', msg)
				raise forms.ValidationError(msg)
			elif ( (start_date == today <= end_date) and
					not(now.time() < start_hour < end_hour) ):
				msg = _('Invalid booking hours: Time must be after'
						' current hour')
				self.add_error('start_hour', msg)
				self.add_error('end_hour', msg)
				raise forms.ValidationError(msg)
		except Exception as e:
			msg = _('Inputs are invalid')
			print(e)
			traceback.print_exc()
			raise forms.ValidationError(msg)
