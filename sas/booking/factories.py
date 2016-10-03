from factory.django import DjangoModelFactory
from booking.models import *
from faker import Factory as FakerFactory
from factory import *
import factory
from factory.fuzzy import FuzzyChoice

fake = FakerFactory.create()

class PlaceFactory(DjangoModelFactory):

	class Meta:
		model = Place
		django_get_or_create = ('name', 'capacity', 'is_laboratory')

	name = factory.Sequence(lambda x: 'I%s' % x)
	capacity = factory.Sequence(lambda x: '%s' % x)
	is_laboratory = False
