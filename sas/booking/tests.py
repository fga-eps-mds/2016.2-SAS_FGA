from django.test import TestCase
from booking.models import BookTime
from datetime import datetime


class TestBookTime(TestCase):

    def test_get_str_weekday(self):
        book = BookTime()
        book.date_booking = datetime.strptime("21092016", "%d%m%Y")
        self.assertEqual(book.get_str_weekday(), "Wednesday")
