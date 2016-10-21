from django.test import TestCase, RequestFactory
from booking.models import *
from django.test import Client
from booking.factories import *
from datetime import datetime
from user.factories import UserFactory, UserProfileFactory
from booking.views import new_booking
from booking.forms import BookingForm

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

    def test_form_is_valid(self):
        form = BookingForm(data=self.parameters)
        self.assertTrue(form.is_valid())

class TestBookTime(TestCase):

	def test_get_str_weekday(self):
		book = BookTime()
		book.date_booking = datetime.strptime("21092016", "%d%m%Y")
		self.assertEqual(book.get_str_weekday(), "Wednesday")
