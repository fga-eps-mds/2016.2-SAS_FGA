from django.test import TestCase, RequestFactory
from booking.models import *
from django.test import Client
from booking.factories import *
from datetime import datetime, timedelta
from user.factories import UserFactory
from booking.forms import SearchBookingForm
from dateutil import parser

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
        days.append(start_date)
        days.append(end_date)
        days2 = form.days_list()
        self.assertEqual(days,days2)
   
    '''def test_search(self):
        start_date = parser.parse(2018-10-10)
        end_date = parser.parse(2018-10-11)
        building_name = Building.objects.get(name='UAC')
        room_name = Place.objects.get(pk=8)
        parameters = {'search_options': 'opt_room_period','building_name': building_name,
            'room_name' : room_name, 'start_date' : start_date}
        form = SearchBookingForm(data=parameters)'''
