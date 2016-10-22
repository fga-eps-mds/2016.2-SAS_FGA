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
        #creating user
        user1 = UserProfile()
        user1.user = User()
        user1.registration_number = "123456789"
        user1.user.email = "email@email.com"
        user1.user.username = "email@email.com"
        user1.user.first_name = "email"
        user1.user.set_password("123456")
        user1.save()
        #creating booking
        booking1 = Booking()
        booking1.user = User()
        booking1.user = User.objects.get(username="email@email.com")
        booking1.name = "monitoria"
        booking1.start_date = datetime.strptime("21092017", "%d%m%Y").date()
        booking1.end_date = datetime.strptime("22092017", "%d%m%Y").date()
        booking1.place = Place()
        booking1.place.name = "FGA-I1"
        booking1.place.building = Building()
        booking1.place.building.name = "UAC"
        booking1.save()
        #creating booktime
        book1 = BookTime()
        book1.date_booking = parser.parse("2017-09-21")
        book1.start_hour = "20:00"
        book1.end_hour = "22:00"
        book1.save()
        booking1.time.add(book1)
        booking1.save()
        book2 = BookTime() 
        book2.date_booking = parser.parse("2017-09-23")
        book2.start_hour = "20:00"
        book2.end_hour = "22:00"
        book2.save()
        booking1.time.add(book2)
        booking1.save()
        #creating form
        start_date=datetime.strptime("21092017", "%d%m%Y").date()
        end_date=datetime.strptime("21092017", "%d%m%Y").date()
        building_name = Building.objects.get(name='UAC')
        room_name = Place.objects.get(name="FGA-I1")
        parameters = {'search_options' : 'opt_room_period', 'building_name': building_name, 'room_name' : room_name,
            'start_date' : start_date, 'end_date' : end_date}
        form = SearchBookingForm(data=parameters)
        #test
        form.is_valid()
        bookings_test = []
        bookings_test.append(booking1)
        bookings_search = form.search()
        self.assertEqual(bookings_test,bookings_search)
