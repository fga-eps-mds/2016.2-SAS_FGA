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
from user.models import UserProfile

class TestBookTime(TestCase):

	def test_get_str_weekday(self):
		book = BookTime()
		book.date_booking = datetime.strptime("21092016", "%d%m%Y")
		self.assertEqual(book.get_str_weekday(), "Wednesday")

class DeleteBookingTest(TestCase):

    def setUp(self):
        self.user = UserProfileFactory.create()
        self.user.user.set_password('1234567')
        self.user.save()
        self.booking = BookingFactory.create()
        print(self.booking.user.id)
        self.booking.user = self.user.user
        print(self.user.id)
        print(self.booking.user.id)
        self.booktimes = [BookTimeFactory.create() for x in range(5)]
        self.booking = BookingFactory.create(booktimes = self.booktimes)
        self.booking.save()
        self.client = Client()

    def test_admin_delete_booking(self):
        self.user.make_as_admin()
        self.client.login(username = self.user.user.username, password = '1234567')
        url = reverse('booking:deletebooking', args = (self.booking.id,))
        response = self.client.get(url)
        for booktime in self.booktimes:
            self.assertFalse(BookTime.objects.filter(pk = booktime.id).exists())
        self.assertFalse(Booking.objects.filter(pk = self.booking.id).exists())
        self.assertContains(response, 'Booking deleted!')

    def test_academic_staff_delete_their_own_booking(self):
        self.user.make_as_academic_staff()
        self.user.save()
        self.booking.user = self.user.user
        self.booking.save()
        self.client.login(username = self.user.user.username, password = '1234567')
        url = reverse('booking:deletebooking', args = (self.booking.id,))
        response = self.client.get(url)
        self.assertContains(response, 'Booking deleted!')

    def test_doesnt_have_permission(self):
        self.user.make_as_academic_staff()
        self.client.login(username = self.user.user.username, password = '1234567')
        booking = BookingFactory.create()
        url = reverse('booking:deletebooking', args = (booking.id,))
        response = self.client.get(url)
        self.assertContains(response, 'You cannot delete this booking.')

    def test_user_not_logged_in(self):
        url = reverse('booking:deletebooking', args = (self.booking.id,))
        response = self.client.get(url)
        self.assertContains(response, 'You are not logged in.')

    def test_booking_does_not_exist(self):
        self.client.login(username = self.user.user.username, password = '1234567')
        url = reverse('booking:deletebooking', args = (9999,))
        response = self.client.get(url)
        self.assertContains(response, 'Booking not found.')

class DeleteBooktimeTest(TestCase):

    def setUp(self):
        self.user = UserFactory.create()
        self.user.set_password('1234567')
        self.user.save()
        self.booktimes = [BookTimeFactory.create()]
        self.booking = BookingFactory.create(booktimes = self.booktimes)
        self.booking.user = self.user
        self.booking.save()
        self.client = Client()

    def test_delete_booktime(self):
        self.client.login(username = self.user.username, password = '1234567')
        url = reverse('booking:deletebooktime', args = [self.booking.id, self.booktimes[0].id])
        response = self.client.get(url)
        self.assertFalse(BookTime.objects.filter(pk = self.booktimes[0].id).exists())
        self.assertFalse(Booking.objects.filter(pk = self.booking.id).exists())
        self.assertContains(response, 'Booking deleted!')

    def test_doesnt_have_permission(self):
        #self.client.login(username = self.user.username, password = '1234567')
        url = reverse('booking:deletebooktime', args = (self.booking.id, self.booktimes[0].id))
        response = self.client.get(url)
        self.assertContains(response, 'You cannot delete this booking.')

    def test_user_not_logged_in(self):
        url = reverse('booking:deletebooktime', args = (self.booking.id, self.booktimes[0].id))
        response = self.client.get(url)
        self.assertContains(response, 'You cannot delete this booking.')
