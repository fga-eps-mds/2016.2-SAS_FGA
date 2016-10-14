from factory.django import DjangoModelFactory
from booking.models import *
from faker import Factory as FakerFactory
from factory import *
import factory
<<<<<<< HEAD
=======
import radar
>>>>>>> Created booktime factory and fixed booking factory.
from factory.fuzzy import FuzzyChoice, FuzzyDate, FuzzyInteger
from user.factories import UserFactory
from datetime import date, datetime, time
from random import randrange, randint

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
		django_get_or_create = ('place', 'name', 'start_date', 'end_date')

	place = FuzzyChoice(SPACES)
	name = factory.LazyAttribute(lambda x: fake.name())
	start_date = FuzzyDate(datetime(2017, 1, 1), datetime(2017, 5, 31))
	end_date = FuzzyDate(datetime(2017, 6, 1), datetime(2017, 12, 31))

	@factory.post_generation
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

	start_hour = time(hour = randint(0, 23), minute = randrange(0, 50, 10))
	end_hour = time(hour = randint(int(start_hour.hour), 23), minute = randrange(0, 50, 10))
	date_booking = FuzzyDate(datetime(2017, 1, 1), datetime(2017, 12, 31))
