from django.utils.translation import ugettext_lazy as _, ugettext as __
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

CATEGORY = (('1', _('Student')),
			('2', _('Teaching Staff')), ('3', _('Employees')))


class UserProfile(models.Model):
	registration_number = models.CharField(max_length=20)
	user = models.OneToOneField(User, on_delete=models.CASCADE,
								related_name="profile_user")
	category = models.CharField(choices=CATEGORY, max_length=20)

	def name(self, name):
		if self.user is None:
			self.user = User()
		names = name.split()
		self.user.first_name = names.pop(0)
		self.user.last_name = str.join(" ", names)

	def full_name(self):
		name = str.join(" ", [self.user.first_name, self.user.last_name])
		return name

	def save(self, *args, **kwargs):
		self.user.save()
		self.user_id = self.user.pk
		super(UserProfile, self).save(*args, **kwargs)

class Place(models.Model):
	name = models.CharField(max_length=50)
	capacity = models.CharField(max_length=250)
	is_laboratory = models.BooleanField()
	place_id = models.CharField(max_length=7)
	localization = models.CharField(max_length=50)

	def save(self, *args, **kwargs):
		super(Place, self).save(*args, **kwargs)

class BookTime(models.Model):
	start_hour = models.TimeField(null=False, blank=False)
	end_hour = models.TimeField(null=False, blank=False)
	start_date = models.DateField(null=False, blank=False)
	end_date = models.DateField(null=False, blank=False)

	def save(self, *args, **kwargs):
		super(BookTime, self).save(*args, **kwargs)

class Booking(models.Model):
	user = models.ForeignKey(User, related_name="bookings", on_delete=models.CASCADE)
	time = models.ManyToManyField(BookTime, related_name="booking_time")
	place = models.ForeignKey(Place, related_name="booking_place") 
	name = models.CharField(max_length=50)

	def save(self, *args, **kwargs):
		super(Booking, self).save(*args, **kwargs)
