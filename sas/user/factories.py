from factory.django import DjangoModelFactory
from faker import Factory as FakerFactory
from factory import *
import factory
from factory.fuzzy import FuzzyChoice
from .models import *

fake = FakerFactory.create()


class UserFactory(DjangoModelFactory):

    class Meta:
        model = User
        django_get_or_create = ('email', 'first_name', 'last_name', 'username')

    email = factory.LazyAttribute(lambda x: fake.email())
    username = factory.LazyAttribute(lambda x: '%s' % x.email)
    first_name = factory.LazyAttribute(lambda x: fake.first_name())
    last_name = factory.LazyAttribute(lambda x: fake.last_name())


class UserProfileFactory(DjangoModelFactory):

    class Meta:
        model = UserProfile
        django_get_or_create = ('registration_number', 'user', 'category')

    category = FuzzyChoice(CATEGORY)
    user = factory.SubFactory(UserFactory)
    registration_number = factory.Sequence(lambda x: '11003055%s' % x)

