from django.test import TestCase, RequestFactory
from booking.models import *
from django.test import Client
from booking.factories import *
from datetime import datetime
from user.factories import UserFactory
from booking.views import search_booking_booking_name_week

class TestBookTime(TestCase):
    def setup(self):
        self.factory = RequestFactory()

    def test_get_str_weekday(self):
        book = BookTime()
        book.date_booking = datetime.strptime("21092016", "%d%m%Y")
        self.assertEqual(book.get_str_weekday(), "Wednesday")

    def test_search_booking_booking_name_week(self):
        factory = self.factory
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=7)

        parameters = {'search_options': 'opt_booking_week','booking_name': 'GPP',
        'start_date' : start_date , 'end_date':end_date}
        form = SearchBookingForm(data=parameters)
        
        print(end_date)

        form.is_valid()
        request = self.factory.post('/booking/searchbookingg/', parameters)
        page = search_booking_booking_name_week(request=request,form_booking=form)
        self.assertEqual(page.status_code, 202)
        self.assertContains(page,'GPPP')