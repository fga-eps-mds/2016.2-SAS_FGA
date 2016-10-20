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
from booking.views import delete_booking
from booking.urls import *

class TestBookTime(TestCase):

	def test_get_str_weekday(self):
		book = BookTime()
		book.date_booking = datetime.strptime("21092016", "%d%m%Y")
		self.assertEqual(book.get_str_weekday(), "Wednesday")

class BookingTest(TestCase):

    def setUp(self):
        self.user = UserFactory.create()
        self.user.set_password('1234567')
        self.user.save()
        self.booktimes = [BookTimeFactory.create() for x in range(5)]
        self.booking = BookingFactory.create(booktimes = self.booktimes)
        self.booking.user = self.user
        self.booking.save()
        self.client = Client()

    def test_has_permission_delete_booking(self):
        self.client.login(username = self.user.username, password = '1234567')
        url = reverse('booking:deletebooking', args = (self.booking.id,))
        #print(Booking.objects.get(pk = self.booking.id))
        response = self.client.get(url)
        for booktime in self.booktimes:
            self.assertFalse(BookTime.objects.filter(pk = booktime.id).exists())
        self.assertFalse(Booking.objects.filter(pk = self.booking.id).exists())
        self.assertContains(response, 'Booking deleted!')
