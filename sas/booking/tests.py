from django.test import TestCase
from booking.models import *
from django.test import Client
from booking.factories import *
from datetime import datetime
from user.factories import UserFactory

class TestBookTime(TestCase):

	def test_get_str_weekday(self):
		book = BookTime()
		book.date_booking = datetime.strptime("21092016", "%d%m%Y")
		self.assertEqual(book.get_str_weekday(), "Wednesday")

class TestSearchBooking(TestCase):
	def setUp(self):
		self.user = UserFactory.create()
		self.user.set_password('1234567')
		self.user.save()
		self.client = Client()
		self.building = Building()
		self.building.name = "UAC"
		self.building.save()
		self.place = Place()
		self.place.building = self.building
		self.place.name = 'FGA-I1'
		self.place.capacity = 40
		self.place.location = 'teste'
		self.place.place_id = 'oi'
		self.place.is_laboratory = False
		self.place.save()
		self.booking = Booking()
		self.booking.place = self.place
		self.booking.name = 'Teste'
		self.booking.building = self.building
		self.booking.start_date = '2020-10-20'
		self.booking.end_date = '2020-10-28'
		self.booking.booking_time = BookTime()
		self.booking.booking_time.start_hour = '08:00:00'
		self.booking.booking_time.end_hour = '10:00:00'
		self.booking.booking_time.date_booking = '2020-10-21'
		self.booking.user = self.user
		self.booking.save()
	def test_get_request(self):
		response = self.client.get('/booking/searchbookingg/')
		self.assertEqual(response.status_code, 200)

	def test_search_booking_post_not_valid(self):
		client = self.client
		parameters = {'search_options': 'opt_day_room','building_name': 'UAC',
			'room_name' : 'UAC | FGA-I1', 'start_date' : '10/20/1990'}
		response = client.post('/booking/searchbookingg/', parameters)
		self.assertTemplateUsed(response, 'booking/searchBookingQuery.html')
