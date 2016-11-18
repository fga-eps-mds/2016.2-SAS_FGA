from django.utils.translation import ugettext_lazy as _, ugettext as __
from django.db import models, connection
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
import copy
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

CATEGORY = (('', '----'), ('1', _('Student')),
            ('2', _('Teaching Staff')), ('3', _('Employees')))

WEEKDAYS = (('0', _("Monday")), ('1', _("Tuesday")), ('2', _("Wednesday")),
            ('3', _("Thursday")), ('4', _("Friday")), ('5', _("Saturday")),
            ('6', _("Sunday")))

ENGINEERING = (('0', _("Select the Engineering")), ('1', _("Aerospace Engineering")), 
            ('2', _("Automotive Engineering")), ('3', _("Electronic Engineering")), 
            ('4', _("Energy Engineering")), ('5', _("Software Engineering")),
            ('6', _("Engineerings")))


class Building(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Place(models.Model):
    name = models.CharField(max_length=200)
    capacity = models.PositiveSmallIntegerField()
    building = models.ForeignKey(Building, related_name='building')
    location = models.CharField(max_length=50)
    place_id = models.CharField(max_length=200)
    is_laboratory = models.BooleanField(default=False)

    def __str__(self):
        try:
            return (self.building.name + " | " + self.name +
                    " - Cap. " + str(self.capacity))
        except:
            return self.name


class BookTime(models.Model):
    start_hour = models.TimeField(null=False, blank=False)
    end_hour = models.TimeField(null=False, blank=False)
    date_booking = models.DateField(null=False, blank=False)

    def add_days(self, nr_days):
        delta = timedelta(days=nr_days)
        self.date_booking = self.date_booking + delta

    def next_week_day(self, nr_weekday):
        diff_of_weekdays = self.date_booking.weekday() - nr_weekday
        if diff_of_weekdays > 0:
            self.add_days(7 - diff_of_weekdays)
        elif diff_of_weekdays < 0:
            self.add_days(diff_of_weekdays * (-1))
        else:
            self.add_days(7)

    def get_str_weekday(self):
        return self.date_booking.strftime("%A")

    def __str__(self):
        return (str(self.date_booking) + " | " +
                str(self.start_hour) + " - " + str(self.end_hour))

    def delete_booktime(self, booking):
        if booking.time.count() == 1:
            booking.delete()
        else:
            booking.time.remove(self)
            super(BookTime, self).delete()

BOOKING_STATUS = ((0, _("Denied")), (1, _("Pending")), (2, _("Approved")))


class Booking(models.Model):
    user = models.ForeignKey(User, related_name="bookings",
                             on_delete=models.CASCADE)
    responsible = models.CharField(max_length=100, default=' ')
    time = models.ManyToManyField(BookTime, related_name="booking_time")
    place = models.ForeignKey(Place, related_name="booking_place")
    name = models.CharField(max_length=50)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    status = models.PositiveSmallIntegerField(choices=BOOKING_STATUS,
                                              default=2)

    engineering = models.CharField(choices=ENGINEERING, max_length=5)

    def __str__(self):
        return (self.name + " " + self.user.email + " | " + str(self.place) +
                " - " + str(self.start_date) + " - " + str(self.end_date))

    def exists(self, start_hour, end_hour, week_days):
        str_weekdays = []
        if not week_days:
            return True
        for day in week_days:
                new_day = int(day) + 1 % 6
                str_weekdays.append("'" + str(new_day) + "'")

        str_weekdays = ",".join(str_weekdays)
        sql = """select count(*) from booking_booking_time bbt
               inner join booking_booktime bt on bbt.booktime_id = bt.id
               inner join booking_booking bb on bbt.booking_id = bb.id
               inner join booking_place bp on bb.place_id = bp.id"""
        sql += " where bt.date_booking >= date('" + (
               self.start_date.strftime("%Y-%m-%d") + "')")
        sql += " and bt.date_booking <= date('" + (
               self.end_date.strftime("%Y-%m-%d") + "')")
        sql += " and bt.start_hour <= time('" + (
               start_hour.strftime("%H:%M:%S") + "')")
        sql += " and bt.end_hour >= time('" + (
               end_hour.strftime("%H:%M:%S") + "')")
        sql += " and bb.status = 2"
        sql += " and strftime('%w',bt.date_booking) IN (" + str_weekdays + ")"
        sql += " and bp.id = '" + str(self.place.pk) + "'"

        with connection.cursor() as cursor:
            cursor.execute(sql)
            row = cursor.fetchone()
        if row[0] > 0:
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        if (self.place.is_laboratory and not
                self.user.profile_user.is_admin()):
            self.status = 1  # status for pending booking
        if Place.objects.filter(name=self.place.name):
            self.place = Place.objects.get(name=self.place.name)
        else:
            self.place.save()
            self.place_id = self.place.pk
        super(Booking, self).save(*args, **kwargs)

    def delete(self):
        self.time.all().delete()
        super(Booking, self).delete()

    def update_status(self, status):
        Booking.objects.filter(pk=self.pk).update(status=status)
        self.refresh_from_db()

    def update_start_date(self):
        all_booktimes = self.time.order_by('date_booking')
        self.start_date = all_booktimes.first().date_booking
        self.save()

    def update_end_date(self):
        all_booktimes = self.time.order_by('date_booking')
        self.end_date = all_booktimes.last().date_booking
        self.save()

    def delete_booktime(self, id_booktime, user):
        booktime = BookTime.objects.get(pk=id_booktime)
        all_booktimes = self.time.order_by('date_booking')
        if (user.profile_user.is_admin() or self.user.id == user.id) and \
                booktime in all_booktimes:
            booktime.delete()
            if(all_booktimes.count() > 1):
                self.update_start_date()
                self.update_end_date()
        else:
            raise PermissionDenied()

    @staticmethod
    def get_bookings():
        bookings = Booking.objects.values('name').order_by('-name').distinct()
        choices = ()
        for booking in bookings:
            new_choice = (booking['name'], booking['name'])
            choices = (new_choice,) + choices
        return choices


class Validation():

    def hasNumbers(self, string):
        if any(char.isdigit() for char in string):
            return True

    def hasLetters(self, number):
        if any(char.isalpha() for char in number):
            return True

    def hasSpecialCharacters(self, string):
        for character in '@#$%^&+=/\{[]()}-_+=*!§|':
            if character in string:
                return True


def date_range(start_date, end_date):
    return [start_date + timedelta(days=x)
            for x in range(0, (end_date - start_date).days + 1)]
