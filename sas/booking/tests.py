from django.test import TestCase
from booking.models import *
from django.test import Client
from booking.factories import *
from datetime import datetime
from user.factories import UserFactory
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
