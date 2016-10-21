from django.test import TestCase, RequestFactory
from booking.models import *
from django.test import Client
from booking.factories import *
from user.factories import UserFactory
from booking.forms import SearchBookingForm
from booking.views import search_booking_day_room
from datetime import datetime, timedelta

class TestBookTime(TestCase):

    def test_get_str_weekday(self):
        book = BookTime()
        book.date_booking = datetime.strptime("21092016", "%d%m%Y")
        self.assertEqual(book.get_str_weekday(), "Wednesday")

class TestSearchBooking(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_request(self):
        response = self.client.get('/booking/searchbookingg/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/searchBookingQuery.html')


    def test_search_booking_post_not_valid(self):
        client = self.client
        start_date = datetime.now().date() - timedelta(days=6)
        building_name = Building.objects.filter(name='UAC')
        room_name = Place.objects.filter(pk=8)
        parameters = {'search_options': 'opt_day_room','building_name': building_name,
            'room_name' : room_name, 'start_date' : start_date}
        response = client.post('/booking/searchbookingg/', parameters)
        self.assertTemplateUsed(response, 'booking/searchBookingQuery.html')




class TestBookTime(TestCase):

	def test_get_str_weekday(self):
		book = BookTime()
		book.date_booking = datetime.strptime("21092016", "%d%m%Y")
		self.assertEqual(book.get_str_weekday(), "Wednesday")


class TestSearchBookingQuery(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    def test_count_days(self):
        form = SearchBookingForm()
        start_date=datetime.strptime("21092016", "%d%m%Y")
        end_date=datetime.strptime("22092016", "%d%m%Y")
        days = [start_date,end_date]
        days2 = form.count_days(start_date=start_date,end_date=end_date)
        self.assertEqual(days,days2)

    def test_search_booking_day_room(self):
        factory = self.factory
        start_date = datetime.now().date()
        building_name = Building.objects.filter(name='UAC')
        room_name = Place.objects.filter(pk=8)
        parameters = {'search_options': 'opt_day_room','building_name': building_name,
            'room_name' : room_name, 'start_date' : start_date}
        form = SearchBookingForm(data=parameters)
        if form.is_valid():
            request = factory.post('/booking/searchbookingg', parameters)
            page = search_booking_day_room(request=request,form_booking=form)
            self.assertEqual(page.status_code,200)
            self.assertContains(page, "Room x Day")
    def test_form_is_valid(self):
        start_date = datetime.now().date()
        building_name = Building.objects.filter(name='UAC')
        room_name = Place.objects.filter(pk=8)
        parameters = {'search_options': 'opt_day_room','building_name': building_name,
			'room_name' : room_name, 'start_date' : start_date}
        form = SearchBookingForm(data=parameters)
        self.assertTrue(form.is_valid())
