from django.utils.translation import ugettext_lazy as _
from booking.models import (WEEKDAYS, Booking, BookTime, Place, Building,
                            date_range, Validation, Tag)
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from datetime import date, datetime, timedelta, time
from django.conf import settings
from django.utils import formats
from user.models import UserProfile
import copy
import re
import traceback
import ast


class SearchBookingForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(SearchBookingForm, self).__init__(*args, **kwargs)
        self.fields['booking_name'] = forms.ChoiceField(
            choices=Booking.get_bookings(),
            label=_('Booking:'),
            required=False,
            widget=forms.widgets.Select(
                attrs={'class': 'select2 optional'})
        )

        self.fields['responsible'] = forms.CharField(
            label=_('Responsible:'),
            required=False,
            widget=forms.widgets.Select(
                attrs={'class': 'select2 optional'},
                choices=Booking.get_responsibles(),)
        )

    SEARCH_CHOICES = (
        ('opt_day_room', _("Room's Week Timetable")),
        ('opt_booking_week', _(' Booking')),
        ('opt_building_day', _(' Occupation')),
        ('opt_room_period', _(' Room ')),
        ('opt_responsible', _(' Responsible')),
    )

    search_options = forms.ChoiceField(label=_('Search options'),
                                       choices=SEARCH_CHOICES,
                                       widget=forms.RadioSelect())

    building_name = forms.ModelChoiceField(
        queryset=Building.objects,
        label=_('Building:'), required=False,
        widget=forms.widgets.Select(
            attrs={'class': 'optional'}))

    room_name = forms.ModelChoiceField(
        queryset=Place.objects,
        label=_('Place:'),
        required=False,
        widget=forms.widgets.Select(
            attrs={'class': 'optional'}))

    start_date = forms.DateField(
        label=_('Date:'),
        widget=forms.widgets.DateInput(
            attrs={'class': 'datepicker1 optional', 'placeholder': ''}),
        required=False)

    end_date = forms.DateField(
        label=_('Date (To):'),
        widget=forms.widgets.DateInput(
            attrs={'class': 'datepicker1 optional', 'placeholder': ''}),
        required=False)

    def search(self):
        cleaned_data = super(SearchBookingForm, self).clean()
        all_bookings = Booking.objects.all()
        end_date = self.cleaned_data.get('end_date')
        start_date = self.cleaned_data.get('start_date')
        bookings = []

        for booking in all_bookings:
            if not(booking.end_date < start_date or
                   booking.start_date > end_date):
                bookings.append(booking)

        return bookings

    def count_days(self, start_date, end_date):

        days = []
        while(start_date <= end_date):
            days.append(start_date)
            start_date += timedelta(days=1)

        return days

    def days_list(self):

        cleaned_data = super(SearchBookingForm, self).clean()
        end_date = self.cleaned_data.get('end_date')
        start_date = self.cleaned_data.get('start_date')
        days = self.count_days(start_date=start_date, end_date=end_date)

        return days

    def week_day(self):
        cleaned_data = super(SearchBookingForm, self).clean()
        start_date = self.cleaned_data.get('start_date')
        weekday_start_date = start_date.weekday()
        monday = start_date - timedelta(days=weekday_start_date)
        sunday = monday + timedelta(days=6)
        days = self.count_days(start_date=monday, end_date=sunday)

        return days

    def get_day(self):
        cleaned_data = super(SearchBookingForm, self).clean()
        start_date = self.cleaned_data.get('start_date')

        return start_date

    def clean(self):
        cleaned_data = super(SearchBookingForm, self).clean()
        today = date.today()
        now = datetime.now()

        try:
            option = self.cleaned_data.get('search_options')
            start_date = self.cleaned_data.get('start_date')

            if(option == 'opt_room_period' or option == 'opt_booking_week'):
                end_date = self.cleaned_data.get('end_date')

                if not(today <= start_date and today <= end_date):
                    msg = _('Invalid booking period: \
                             Booking must be in future date')

                    self.add_error('start_date', msg)
                    raise forms.ValidationError(msg)
                if not(today <= end_date):
                    msg = _('End date must be from future date')
                    self.add_error('end_date', msg)
                    raise forms.ValidationError(msg)

                elif(end_date < start_date):
                    msg = _('End date must be equal or \
                             greater then Start date')

                    self.add_error('start_date', msg)
                    self.add_error('end_date', msg)
                    raise forms.ValidationError(msg)
                booking = self.search()
                if not booking:
                    msg = _('Doesnt exist any booking in \
                             this period of time')
                    self.add_error('start_date', msg)
                    self.add_error('end_date', msg)
                    raise forms.ValidationError(msg)

        except Exception as e:
            msg = _('Fill all the fields correctly')
            print(e)
            raise forms.ValidationError(msg)


class BookingForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['responsible'] = forms.CharField(
            label=_('Responsible (optional):'),
            required=False,
            widget=forms.widgets.Select(
                attrs={'class': 'selectize'},
                choices=UserProfile.get_users(),
            )
        )
        self.fields['tags'] = forms.CharField(
            label=_('Tags (optional):'),
            required=False,
            widget=forms.widgets.SelectMultiple(
                attrs={'class': 'selectize_multiple'},
                choices=Tag.get_tags(),
            )
        )
    hour = datetime.strptime("08:00", "%H:%M").time()
    hour2 = datetime.strptime("10:00", "%H:%M").time()
    hour3 = datetime.strptime("12:00", "%H:%M").time()
    hour4 = datetime.strptime("14:00", "%H:%M").time()
    hour5 = datetime.strptime("16:00", "%H:%M").time()
    hour6 = datetime.strptime("18:00", "%H:%M").time()
    hour7 = datetime.strptime("20:00", "%H:%M").time()
    hour8 = datetime.strptime("22:00", "%H:%M").time()
    hour9 = datetime.strptime("00:00", "%H:%M").time()
    HOURS = (('', '----'), (hour, '08:00'), (hour2, ('10:00')),
             (hour3, ('12:00')), (hour4, ('14:00')),
             (hour5, ('16:00')), (hour6, ('18:00')),
             (hour7, ('20:00')), (hour8, ('22:00')),
             (hour9, ('00:00')))

    DATE_CHOICES = (
        ('opt_date_semester', _("Yes")),
        ('opt_select_date', _("No")),
    )

    name = forms.CharField(
        label=_('Booking Name:'),
        widget=forms.TextInput(attrs={'placeholder': ''}))
    date_options = forms.ChoiceField(label=_('Do you wish to register booking \
                                                for a semester?'),
                                     choices=DATE_CHOICES,
                                     widget=forms.RadioSelect())
    start_date = forms.DateField(
        label=_('Start Date:'),
        required=False,
        widget=forms.widgets.DateInput(
            attrs={'class': 'datepicker1', 'placeholder': _("mm/dd/yyyy")}))
    end_date = forms.DateField(
        label=_('End Date:'),
        required=False,
        widget=forms.widgets.DateInput(
            attrs={'class': 'datepicker1', 'placeholder': _("mm/dd/yyyy")}))
    start_hour = forms.TimeField(
        label=_('Start Time:'),
        widget=forms.Select(choices=HOURS))
    end_hour = forms.TimeField(
        label=_('End Time:'),
        widget=forms.Select(choices=HOURS))

    building = forms.ModelChoiceField(
        queryset=Building.objects,
        label=_('Building:'))
    place = forms.ModelChoiceField(
        queryset=Place.objects,
        label=_('Place:'))
    week_days = forms.MultipleChoiceField(
        label=_("Days of week: "),
        required=False,
        choices=WEEKDAYS,
        widget=forms.CheckboxSelectMultiple())

    def save(self, user, force_insert=False, force_update=False, commit=True):
        booking = Booking()
        booking.user = user
        booking.name = self.cleaned_data.get("name")
        booking.start_date = self.cleaned_data.get("start_date")
        booking.end_date = self.cleaned_data.get("end_date")
        booking.place = self.cleaned_data.get("place")
        weekdays = self.cleaned_data.get("week_days")

        if user.profile_user.is_admin():
            booking.responsible = self.cleaned_data.get("responsible")
            name = re.search('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
                             booking.responsible)
            if name is not None:
                name = name.group()
            users = User.objects.filter(username=name)
            ONE_FOUND = 1
            if user.profile_user.is_admin() and (users.count() is ONE_FOUND):
                booking.user = users[0]
        else:
            booking.responsible = str(user.profile_user)

        book = BookTime()
        book.date_booking = booking.start_date
        book.start_hour = self.cleaned_data.get("start_hour")
        book.end_hour = self.cleaned_data.get("end_hour")
        try:
            booking.save()
            if booking.exists(book.start_hour, book.end_hour, weekdays):
                booking.delete()
                return None
            else:
                for day in date_range(book.date_booking, booking.end_date):
                    if(day.isoweekday() - 1 in map(int, weekdays)):
                        newBookTime = BookTime(start_hour=book.start_hour,
                                               end_hour=book.end_hour,
                                               date_booking=day)
                        newBookTime.save()
                        booking.time.add(newBookTime)
                tags = self.cleaned_data['tags']
                if tags:
                    tags = ast.literal_eval(tags)
                    for name in tags:
                        if not Tag.objects.filter(name=name).exists():
                            tag = Tag(name=name)
                            tag.save()
                        tag = Tag.objects.get(name=name)
                        booking.tags.add(tag)
                booking.save()
        except Exception as e:
            booking.delete()
            msg = _('Failed to book selected period')
            print(e)
            raise forms.ValidationError(msg)
            return None
        return booking
        # do custom stuff

    def clean_week_days(self):
        weekdays = self.cleaned_data['week_days']
        try:
            start_date = self.cleaned_data['start_date']
            end_date = self.cleaned_data['end_date']
            if ((end_date - start_date).days > 7 and
                    not weekdays):  # 7 days in a week
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
            elif ((start_date == today <= end_date) and
                    not(now.time() < start_hour < end_hour)):
                msg = _('Invalid booking hours: Time must be after'
                        ' current hour')
                self.add_error('start_hour', msg)
                self.add_error('end_hour', msg)
                raise forms.ValidationError(msg)
            if(start_hour >= end_hour):
                msg = _('Invalid booking hours: End date must be'
                        ' greater then start date')
                self.add_error('start_hour', msg)
                self.add_error('end_hour', msg)
                raise forms.ValidationError(msg)

        except Exception as e:
            print(e)
            msg = _('Inputs are invalid')
            raise forms.ValidationError(msg)
