from django.test import TestCase, RequestFactory
from booking.models import *
from django.test import Client
from booking.factories import *
from datetime import datetime, timedelta
from user.factories import UserFactory, UserProfileFactory
from booking.views import new_booking, search_booking_day_room
from booking.forms import BookingForm, SearchBookingForm

class TestNewBooking(TestCase):
    def setUp(self):
        self.user = UserProfileFactory.create()
        self.user.user.set_password('1234567')
        self.user.save()
        self.client = Client()
        self.factory = RequestFactory()
        self.week_days = ['3', '5']
        self.start_date=datetime.strptime("21092017", "%d%m%Y")
        self.end_date=datetime.strptime("22092017", "%d%m%Y")
        self.hour = datetime.strptime("08:00", "%H:%M").time()
        self.hour2 = datetime.strptime("10:00", "%H:%M").time()
        self.building_name = Building.objects.filter(name='UAC')
        self.place_name = Place.objects.filter(pk=3)
        self.parameters = {'name': 'Reservaoiasd','start_hour': self.hour, \
            'end_hour' : self.hour2, 'start_date' : self.start_date,
			'end_date': self.end_date,'building': self.building_name,'place': self.place_name, 'week_days': self.week_days}

    def test_get_request_logged(self):
        request = self.factory.get('/booking/newbooking/')
        request.user = self.user.user
        response = new_booking(request)
        self.assertEqual(response.status_code, 200)

    def test_get_request_anonymous(self):
        url = '/booking/newbooking/'
        response = self.client.get(url, follow = True)
        self.assertTemplateUsed(response, 'sas/index.html')


    def test_post_not_valid(self):
        start_date=datetime.strptime("21091999", "%d%m%Y")
        parameters = {'name': 'Reservaoiasd','start_hour': self.hour, \
            'end_hour' : self.hour2, 'start_date' : start_date,
            'end_date': self.end_date,'building': self.building_name,'place': self.place_name, 'week_days': self.week_days}
        request = self.factory.get('/booking/newbooking/', follow=True)
        client = self.client
        username = self.user.user.username
        print(username)
        client.login(username=username, password='1234567')
        response = client.post('/booking/newbooking/', parameters)
        print(response)
        self.assertTemplateUsed(response, 'booking/newBooking.html')

    def test_form_is_valid(self):
        form = BookingForm(data=self.parameters)
        self.assertTrue(form.is_valid())



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
