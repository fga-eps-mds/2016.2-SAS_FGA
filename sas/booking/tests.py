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
        self.user = UserFactory.create()
        self.user.set_password('1234567')
        self.user.save()
        self.booking = BookingFactory.create()
        self.booking.user = self.user
        self.booking.user.save()
        self.booking.save()
        booktimes = [BookTimeFactory.create() for x in range(5)]
        for booktime in booktimes:
            booktime.booking = self.booking
            booktime.save()
        self.booking.save()
        self.booking = BookingFactory.create(time = booktimes)
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
