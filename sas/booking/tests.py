from django.test import TestCase
from booking.models import *
from django.test import Client
from booking.factories import *
from datetime import datetime
from user.factories import UserFactory
from booking.forms import SearchBookingForm

class TestBookTime(TestCase):

	def test_get_str_weekday(self):
		book = BookTime()
		book.date_booking = datetime.strptime("21092016", "%d%m%Y")
		self.assertEqual(book.get_str_weekday(), "Wednesday")


class TestSearchBookingQuery(TestCase):
    def test_count_days(self):
        form = SearchBookingForm()
        start_date=datetime.strptime("21092016", "%d%m%Y")
        end_date=datetime.strptime("22092016", "%d%m%Y")
        days = [start_date,end_date]
        days2 = form.count_days(start_date=start_date,end_date=end_date)
        self.assertEqual(days,days2)
