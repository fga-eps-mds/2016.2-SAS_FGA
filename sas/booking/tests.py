from django.test import TestCase, RequestFactory
from booking.models import *
from django.test import Client
from booking.factories import *
from datetime import datetime, timedelta
from user.factories import UserFactory
from user.models import UserProfile
from booking.forms import SearchBookingForm
from dateutil import parser
from booking.views import search_booking_room_period
from django.db.models import Q

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


    def test_search(self):
        user = UserProfile()
        user.user = User()
        user.registration_number = "123456789"
        user.user.email = "email@email.com"
        user.user.username = "email@email.com"
        user.user.first_name = "email"
        user.user.set_password("123456")
        user.save()

        booking = Booking()
        booking.user = User()
        booking.user = User.objects.get(username="email@email.com")
        booking.name = "monitoria"
        booking.start_date = parser.parse("2017-09-21")
        booking.end_date = parser.parse("2017-09-22")
        booking.place = Place()
        booking.place.name = "FGA-I9"
        booking.place.building = Building()
        booking.place.building.name = "UAC"
        booking.save()

        book = BookTime()
        book.date_booking = parser.parse("2017-09-21")
        book.start_hour = "20:00"
        book.end_hour = "22:00"
        book.save()
        booking.time.add(book)
        booking.save()
        
        start_date=datetime.strptime("21092017", "%d%m%Y")
        end_date=datetime.strptime("22092017", "%d%m%Y")
        building_name = Building.objects.get(name='UAC')
        room_name = Place.objects.get(pk=9)
        parameters = {'search_options' : 'opt_room_period', 'building_name': building_name, 'room_name' : room_name,'start_date' : start_date, 'end_date' : end_date}
        form = SearchBookingForm(data=parameters)
        form.is_valid()

        test = []
        test.append(booking)
        test2 = form.search()
        self.assertEqual(test,test2)
