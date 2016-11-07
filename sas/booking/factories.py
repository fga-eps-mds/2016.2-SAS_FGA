from factory.django import DjangoModelFactory
from booking.models import Building, Place, Booking, BookTime
from faker import Factory as FakerFactory
from factory import *
import factory
from factory.fuzzy import FuzzyChoice, FuzzyDate, FuzzyInteger
from user.factories import UserFactory, UserProfileFactory
from datetime import date, datetime, time
from random import randrange, randint
from django.core.management import call_command

fake = FakerFactory.create()


class BuildingFactory(DjangoModelFactory):

    class Meta:
        model = Building
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda x: 'Building %s' % x)


class PlaceFactory(DjangoModelFactory):

    class Meta:
        model = Place
        django_get_or_create = ('name', 'capacity', 'is_laboratory',
                                'building')

    name = factory.Sequence(lambda x: 'I%s' % x)
    capacity = factory.Sequence(lambda x: '%s' % x)
    is_laboratory = False
    building = factory.SubFactory(BuildingFactory)


class BookTimeFactory(DjangoModelFactory):

    class Meta:
        model = BookTime
        django_get_or_create = ('start_hour', 'end_hour', 'date_booking')

    start_hour = time(hour=randrange(0, 22, 2), minute=randrange(0, 50, 10))
    date_booking = date.today()

    @factory.lazy_attribute
    def end_hour(self):
        hour = randrange(self.start_hour.hour, 22, 2)
        minute = randrange(0, 50, 10)
        return time(hour=hour, minute=minute)


class BookingFactory(DjangoModelFactory):

    class Meta:
        model = Booking
        django_get_or_create = ('user', 'place', 'name', 'start_date',
                                'end_date')

    place = factory.SubFactory(PlaceFactory)
    name = factory.Sequence(lambda x: 'Testando %s' % x)
    start_date = datetime.now()
    end_date = fake.date_time_this_year(before_now=False, after_now=True)

    @factory.lazy_attribute
    def user(self):
        userprofile = UserProfileFactory.create()
        return userprofile.user

    @factory.post_generation
    def times(self, create, extracted, **kwargs):
        if create:
            num_created = 0
            start_date = self.start_date
            while start_date.date() < self.end_date.date() and \
                    start_date.date() != self.end_date.date():
                start_date = fake.date_time_between_dates(start_date,
                                                          self.end_date)
                book = BookTimeFactory(date_booking=start_date)
                book.save()
                self.time.add(book)
