from django.test import TestCase
from booking.models import *
from django.test import Client
from booking.factories import *
from datetime import datetime


class ViewsTest(TestCase):

	def setUp(self):
		self.client = Client()

	def test_index(self):
		result = self.client.get("/")
		self.assertEqual(result.status_code, 200)

	def test_new_user(self):
		result = self.client.get("/user/newuser/")
		self.assertEqual(result.status_code, 200)


class UserProfileTest(TestCase):

	def setUp(self):
		self.userprofile = UserProfile()

	def test_set_name(self):
		self.userprofile.name("Gustavo Rodrigues Coelho")
		self.assertEqual(self.userprofile.user.first_name, "Gustavo")
		self.assertEqual(self.userprofile.user.last_name, "Rodrigues Coelho")

	def test_get_full_name(self):
		name = "Pedro Pereira Pinto"
		self.userprofile.name(name)
		self.assertEqual(self.userprofile.full_name(), name)

	def test_category(self):
		self.assertEqual(len(CATEGORY), 4)

	def test_save(self):
		self.userprofile.name("Gustavo Rodrigues Coelho")
		self.userprofile.registration_number = "11/0030559"
		self.userprofile.user.username = "gutorc@hotmail.com"
		self.userprofile.user.email = "gutorc@hotmail.com"
		self.userprofile.save()
		self.assertEqual(self.userprofile.pk, 1)


class TestBookTime(TestCase):

	def test_add_days(self):
		book = BookTime()
		book.date_booking = datetime.strptime("01022010", "%d%m%Y")
		book.add_days(5)
		self.assertEqual(book.date_booking.strftime("%d%m%Y"), "06022010")

	def test_next_week_day(self):
		book = BookTime()
		book.date_booking = datetime.strptime("21092016", "%d%m%Y")
		book.next_week_day(4)
		self.assertEqual(book.date_booking.strftime("%d%m%Y"), "23092016")
		book.date_booking = datetime.strptime("21092016", "%d%m%Y")
		book.next_week_day(2)
		self.assertEqual(book.date_booking.strftime("%d%m%Y"), "28092016")
		book.date_booking = datetime.strptime("20092016", "%d%m%Y")
		book.next_week_day(0)
		self.assertEqual(book.date_booking.strftime("%d%m%Y"), "26092016")

	def test_get_str_weekday(self):
		book = BookTime()
		book.date_booking = datetime.strptime("21092016", "%d%m%Y")
		self.assertEqual(book.get_str_weekday(), "Wednesday")


class TestBooking(TestCase):

	def setUp(self):
		self.booking = Booking()

	def test_save(self):
		self.booking.user = UserFactory.create()
		self.booking.name = "Teste"
		self.booking.start_date = datetime.now()
		self.booking.end_date = datetime.now()
		self.booking.place = PlaceFactory.create()
		self.booking.save()
		self.assertEqual(self.booking.pk, 1)
