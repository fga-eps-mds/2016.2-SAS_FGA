from django.test import TestCase, RequestFactory
from booking.models import *
from django.test import Client
from booking.factories import *
from datetime import datetime, timedelta
from user.factories import UserFactory
from booking.forms import SearchBookingForm
from dateutil import parser
from booking.views import search_booking_room_period

class TestBookTime(TestCase):
    def test_get_str_weekday(self):
        book = BookTime()
        book.date_booking = datetime.strptime("21092016", "%d%m%Y")
        self.assertEqual(book.get_str_weekday(), "Wednesday")

class TestSearchBookingQuery(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
  
    def test_days_list(self):
        start_date=datetime.strptime("21092017", "%d%m%Y")
        end_date=datetime.strptime("22092017", "%d%m%Y")
        building_name = Building.objects.get(name='UAC')
        room_name = Place.objects.get(pk=9)
        parameters = {'search_options' : 'opt_room_period', 'building_name': building_name, 'room_name' : room_name,
            'start_date' : start_date, 'end_date' : end_date}
        form = SearchBookingForm(data=parameters)
        form.is_valid()
        days = []
        days.append(start_date.date())
        days.append(end_date.date())
        days2 = form.days_list()
        self.assertEqual(days,days2)
   
    def test_search_booking_room_period(self):
        factory = self.factory
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=50)
        building_name = Building.objects.filter(name='UAC')
        room_name = Place.objects.filter(pk=8)
        parameters = {'search_options' : 'opt_room_period', 'building_name' : building_name, 'room_name' : room_name,
            'start_date' : start_date, 'end_date' : end_date}
        form = SearchBookingForm(data=parameters)
        form.is_valid()
        request = factory.post('/booking/searchbookingg', parameters)
        page = search_booking_room_period(request=request,form_booking=form)
        self.assertEqual(page.status_code,200)
        self.assertContains(page, "Room x Period")

