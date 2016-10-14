from factory.django import DjangoModelFactory
from booking.models import *
from faker import Factory as FakerFactory
from factory import *
import factory
import radar
from factory.fuzzy import FuzzyChoice, FuzzyDate, FuzzyInteger
from user.factories import UserFactory
from datetime import date, datetime, time

fake = FakerFactory.create()

class PlaceFactory(DjangoModelFactory):

	class Meta:
		model = Place
		django_get_or_create = ('name', 'capacity', 'is_laboratory')

	name = factory.Sequence(lambda x: 'I%s' % x)
	capacity = factory.Sequence(lambda x: '%s' % x)
	is_laboratory = False

class BookingFactory(DjangoModelFactory):

	class Meta:
		model = Booking
		django_get_or_create = ('user', 'time', 'place', 'name', 'start_date', 'end_date')

	user = factory.SubFactory(UserFactory)
	place = FuzzyChoice(SPACES)
	time = (lambda : [self.booking_time.add(factory.SubFactory(BookTimeFactory)) for counter in range(5)])()
	name = factory.LazyAttribute(lambda x: fake.name())
	start_date = FuzzyDate(datetime.date(2017, 01, 01), datetime.date(2017, 12, 31))
	end_date = FuzzyDate(start_date, datetime.date(2017, 12, 31))

	def booktimes(self, create, extracted, **kwargs):
		if not create:
			return
		if extracted:
			for booktime in extracted:
				self.time.add(booktime)

class BookTimeFactory(DjangoModelFactory):

	class Meta:
		model = BookTime
		django_get_or_create = {'start_hour', 'end_hour', 'date_booking'}

	start_hour = datetime.time(hour = FuzzyInteger(23), minute = FuzzyInteger(50, step = 10))
	end_hour = datetime.time(hour = FuzzyInteger(start_hour.hour, 23), minute = FuzzyInteger(50, step = 10))
