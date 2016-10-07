from django.utils.translation import ugettext as _
from django.forms import ModelForm
from .models import Booking, BookTime, Place, Building
from .models import WEEKDAYS
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import date, datetime, timedelta
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
		if not weekdays:
			date_range = [booking.start_date + timedelta(days=x) for x in range(0, (booking.end_date-booking.start_date ).days)]
			for day in date_range:
				weekdays.append(day.weekday())
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

	def clean_week_days(self):
		weekdays = self.cleaned_data['week_days']
		start_date = self.cleaned_data['start_date']
		end_date = self.cleaned_data['end_date']
		if((end_date-start_date).days > 7 and not weekdays):#7 days in a week
			msg = _('Select a repeating standard for the period you selected')
			self.add_error('week_days', msg)
		return weekdays

	def clean(self):
		cleaned_data = super(BookingForm, self).clean()
		today = date.today()
		now = datetime.now()

		try:
			start_date = cleaned_data.get('start_date')
			end_date = cleaned_data.get('end_date')
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
			msg = _('Inputs are in an invalid format')
			print(e)
			raise forms.ValidationError(msg)
