from django.test import TestCase
from booking.models import *
from django.test import Client
from booking.factories import *
from datetime import datetime
from user.factories import UserFactory, UserProfileFactory
from booking.factories import BookingFactory, BookTimeFactory
from django.urls import reverse
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

class TestBookTime(TestCase):

	def test_get_str_weekday(self):
		book = BookTime()
		book.date_booking = datetime.strptime("21092016", "%d%m%Y")
		self.assertEqual(book.get_str_weekday(), "Wednesday")

class BookingTest(TestCase):

	def setUp(self):
		building = BuildingFactory.create()
		place = PlaceFactory.create()
		place.building = building
		#booktimes = [BookTimeFactory.create() for count in range(5)]
		booktime1 = BookTimeFactory.create()
		booktime2 = BookTimeFactory.create()
		booktime1.place = place
		booktime2.place = place
		booking = BookingFactory.create(time = (booktime1, booktime2))
		self.user = UserProfileFactory.create()
		self.user.user.set_password('1234567')
		self.user.user.save()
		booking.user = self.user
		self.client = Client()
		content_type = ContentType.objects.get_for_model(UserProfile)
		permission = Permission.objects.create(
			codename = 'can_delete',
			name = 'Can delete any booking',
			content_type = content_type,
		)
		#self.user.user.user_permissions.add(permission)

	def test_has_permission_delete_booking(self):
		self.client.login(username = self.user.username, password = '1234567')
		url = reverse('booking:deletebooking', args = (booking.id,))
		response = self.client.get('booking/deletebooking')
		self.assertContains(response, 'Booking deleted!')
