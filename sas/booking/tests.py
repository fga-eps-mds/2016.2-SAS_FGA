from django.test import TestCase
from booking.models import *
from django.test import Client
from booking.factories import *
from datetime import datetime
from user.factories import UserFactory
from booking.factories import BookingFactory, BookTimeFactory
from django.urls import reverse

class TestBookTime(TestCase):

	def test_get_str_weekday(self):
		book = BookTime()
		book.date_booking = datetime.strptime("21092016", "%d%m%Y")
		self.assertEqual(book.get_str_weekday(), "Wednesday")

class BookingTest(TestCase):

	def setUp(self):
		booktimes = [BookTimeFactory.create() for count in range(5)]
		booking = BookingFactory.create(time = booktimes)
		self.user = UserFactory.create()
		self.user.set_password('1234567')
		self.user.save()
		booking.user = self.user
		self.client = Client()
		self.user = book.user

	def has_permission_delete_booking(self):
		self.client.login(username = self.user.username, password = '1234567')
		url = reverse('booking:deletebooking', args = (booking.id,))
		response = self.client.get('booking/deletebooking')
		self.assertContains(response, 'Booking deleted!')
