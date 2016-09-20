from django.test import TestCase
from booking.models import *

class TestBookTime(TestCase):

	def test_add_days(self):
		book = BookTime()
		book.date_booking = datetime.strptime("01022010","%d%m%Y")
		book.add_days(5)
		self.assertEqual(book.date_booking.strftime("%d%m%Y"),"06022010")
	
	def test_next_week_day(self):
		book = BookTime()
		book.date_booking = datetime.strptime("21092016","%d%m%Y")
		book.next_week_day(4)
		self.assertEqual(book.date_booking.strftime("%d%m%Y"),"23092016")
		book.date_booking = datetime.strptime("21092016","%d%m%Y")
		book.next_week_day(2)
		self.assertEqual(book.date_booking.strftime("%d%m%Y"),"21092016")
		book.date_booking = datetime.strptime("20092016","%d%m%Y")
		book.next_week_day(0)
		self.assertEqual(book.date_booking.strftime("%d%m%Y"),"26092016")
