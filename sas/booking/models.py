from django.utils.translation import ugettext_lazy as _, ugettext as __
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

CATEGORY = (('1', _('Student')),('2', _('Teaching Staff')), ('3', _('Employees')))


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

class BookTime(models.Model):
	start_hour = models.TimeField(null=False, blank=False)
	end_hour = models.TimeField(null=False, blank=False)
	start_date = models.DateField(null=False, blank=False)
	end_date = models.DateField(null=False, blank=False)

class Booking(models.Model):
	user = models.OneToOneField(UserProfile, related_name="profile_user")
	time = models.OneToOneField(BookTime, related_name="booking_time")
	place = models.CharField(max_length=50)
	name = models.CharField(max_length=50)
