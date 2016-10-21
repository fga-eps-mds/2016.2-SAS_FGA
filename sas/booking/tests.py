from django.test import TestCase,RequestFactory
from booking.models import *
from django.test import Client
from booking.factories import *
from datetime import datetime
from user.factories import UserFactory
from booking.forms import SearchBookingForm
from booking.views import search_booking_building_day

class TestBookTime(TestCase):

	def test_get_str_weekday(self):
		book = BookTime()
		book.date_booking = datetime.strptime("21092016", "%d%m%Y")
		self.assertEqual(book.get_str_weekday(), "Wednesday")


class TestSearchBookingForm(TestCase):
	
	def setUp(self):
		self.factory = RequestFactory()

	def test_get_day(self):

		start_date = datetime.strptime("12/31/2016", "%m/%d/%Y")
		parameters = {'start_date':start_date}
		booking = SearchBookingForm(data=parameters)

		if booking.is_valid():
			aux = booking.get_day()
			self.assertEqual(start_date,day)

	def test_search_booking_building_day(self):
		factory = self.factory
		
		start_date = datetime.now().date()
		building_name = Building.objects.filter(name='UAC')
		parameters = {'search_options': 'opt_building_day','building_name': building_name,
		'start_date' : start_date}

		form = SearchBookingForm(data=parameters)
		
		if form.is_valid():
			request = self.factory.post('/booking/searchbookingg/', parameters)
			page = search_booking_building_day(request=request,form_booking=form)
			
			self.assertTemplateUsed(page, 'booking/template_table.html')

			