from django.test import TestCase, RequestFactory
from booking.models import *
from django.test import Client
from booking.factories import *
from datetime import datetime, timedelta
from user.factories import UserFactory, UserProfileFactory
from django.urls import reverse
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from booking.views import delete_booking
from booking.views import search_booking_booking_name_week
from booking.views import new_booking, search_booking_day_room
from booking.views import search_booking_building_day
from booking.urls import *
from user.models import UserProfile
from booking.forms import BookingForm, SearchBookingForm
from dateutil import parser
from booking.views import search_booking_room_period
from django.db.models import Q


class TestBookTime(TestCase):
    def test_get_str_weekday(self):
        book = BookTime()
        book.date_booking = datetime.strptime("21092016", "%d%m%Y")
        self.assertEqual(book.get_str_weekday(), "Wednesday")


class TestSearchBookingQuery(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_days_list(self):
        start_date = datetime.strptime("21092017", "%d%m%Y")
        end_date = datetime.strptime("22092017", "%d%m%Y")
        building_name = Building.objects.get(name='UAC')
        room_name = Place.objects.get(pk=9)
        parameters = {'search_options': 'opt_room_period',
                      'building_name': building_name,
                      'room_name': room_name,
                      'start_date': start_date,
                      'end_date': end_date}
        form = SearchBookingForm(data=parameters)
        form.is_valid()
        days = []
        days.append(start_date.date())
        days.append(end_date.date())
        days2 = form.days_list()
        self.assertEqual(days, days2)

    def test_get_str_weekday(self):
        book = BookTime()
        book.date_booking = datetime.strptime("21092016", "%d%m%Y")
        self.assertEqual(book.get_str_weekday(), "Wednesday")


class DeleteBookingTest(TestCase):

    def setUp(self):
        self.user = UserProfileFactory.create()
        self.user.user.set_password('1234567')
        self.user.save()
        self.booking = BookingFactory.create()
        self.booking.user = self.user.user
        self.booktimes = [BookTimeFactory.create() for x in range(5)]
        self.booking = BookingFactory.create(booktimes=self.booktimes)
        self.booking.save()
        self.client = Client()

    def test_admin_delete_booking(self):
        self.user.make_as_admin()
        self.user.save()
        self.client.login(username=self.user.user.username,
                          password='1234567')
        url = reverse('booking:deletebooking', args=(self.booking.id,))
        response = self.client.get(url)
        for booktime in self.booktimes:
            self.assertFalse(BookTime.objects.filter(pk=booktime.id).exists())
        self.assertFalse(Booking.objects.filter(pk=self.booking.id).exists())
        self.assertContains(response, 'Booking deleted!')

    def test_academic_staff_delete_their_own_booking(self):
        self.user.make_as_academic_staff()
        self.user.save()
        self.booking.user = self.user.user
        self.booking.save()
        self.client.login(username=self.user.user.username, password='1234567')
        url = reverse('booking:deletebooking', args=(self.booking.id,))
        response = self.client.get(url)
        self.assertContains(response, 'Booking deleted!')

    def test_doesnt_have_permission(self):
        self.user.make_as_academic_staff()
        self.user.save()
        self.client.login(username=self.user.user.username, password='1234567')
        booking = BookingFactory.create()
        url = reverse('booking:deletebooking', args=(booking.id,))
        response = self.client.get(url)
        self.assertContains(response, 'You cannot delete this booking.')

    def test_user_not_logged_in(self):
        url = reverse('booking:deletebooking', args=(self.booking.id,))
        response = self.client.get(url)
        for booktime in self.booktimes:
            self.assertTrue(BookTime.objects.filter(pk=booktime.id).exists())
        self.assertTrue(Booking.objects.filter(pk=self.booking.id).exists())

    def test_booking_does_not_exist(self):
        self.client.login(username=self.user.user.username, password='1234567')
        url = reverse('booking:deletebooking', args=(9999,))
        response = self.client.get(url)
        self.assertContains(response, 'Booking not found.')


class DeleteBooktimeTest(TestCase):

    def setUp(self):
        self.user = UserProfileFactory.create()
        self.user.user.set_password('1234567')
        self.user.save()
        self.booking = BookingFactory.create()
        self.booking.user = self.user.user
        self.booktimes = [BookTimeFactory.create()]
        self.booking = BookingFactory.create(booktimes=self.booktimes)
        self.booking.save()
        self.client = Client()

    def test_admin_delete_booktime(self):
        self.user.make_as_admin()
        self.user.save()
        self.client.login(username=self.user.user.username,
                          password='1234567')
        url = reverse('booking:deletebooktime',
                      args=[self.booking.id, self.booktimes[0].id])
        response = self.client.get(url)
        self.assertFalse(BookTime.objects.filter(
            pk=self.booktimes[0].id).exists())
        self.assertFalse(Booking.objects.filter(pk=self.booking.id).exists())
        self.assertContains(response, 'Booking deleted!')

    def test_academic_staff_delete_their_own_booktime(self):
        self.user.make_as_academic_staff()
        self.user.save()
        self.booking.user = self.user.user
        self.booking.save()
        self.client.login(username=self.user.user.username,
                          password='1234567')
        url = reverse('booking:deletebooktime',
                      args=(self.booking.id, self.booktimes[0].id))
        response = self.client.get(url)
        self.assertContains(response, 'Booking deleted!')

    def test_doesnt_have_permission(self):
        self.user.make_as_academic_staff()
        self.user.save()
        booktime = [BookTimeFactory.create()]
        booking = BookingFactory.create(booktimes=booktime)
        self.client.login(username=self.user.user.username, password='1234567')
        url = reverse('booking:deletebooktime',
                      args=(booking.id, booktime[0].id))
        response = self.client.get(url)
        self.assertContains(response, 'You cannot delete this booking.')

    def test_user_not_logged_in(self):
        url = reverse('booking:deletebooktime',
                      args=(self.booking.id, self.booktimes[0].id))
        response = self.client.get(url)
        self.assertTrue(BookTime.objects.filter(
            pk=self.booktimes[0].id).exists())
        self.assertTrue(Booking.objects.filter(
            pk=self.booking.id).exists())

    def test_booktime_does_not_exist(self):
        self.client.login(username=self.user.user.username, password='1234567')
        url = reverse('booking:deletebooktime', args=(9999, 9999))
        response = self.client.get(url)
        self.assertContains(response, 'Booking not found.')


class TestNewBooking(TestCase):
    def setUp(self):
        self.user = UserProfileFactory.create()
        self.user.user.set_password('1234567')
        self.user.save()
        self.client = Client()
        self.factory = RequestFactory()
        self.week_days = ['3', '5']
        self.start_date = datetime.strptime("21092017", "%d%m%Y")
        self.end_date = datetime.strptime("22092017", "%d%m%Y")
        self.hour = datetime.strptime("08:00", "%H:%M").time()
        self.hour2 = datetime.strptime("10:00", "%H:%M").time()
        self.building_name = Building.objects.filter(name='UAC')
        self.place_name = Place.objects.filter(pk=3)
        self.parameters = {
            'name': 'Reservaoiasd', 'start_hour': self.hour,
            'end_hour': self.hour2, 'start_date': self.start_date,
            'end_date': self.end_date, 'building': self.building_name,
            'place': self.place_name, 'week_days': self.week_days}

    def test_get_request_logged(self):
        request = self.factory.get('/booking/newbooking/')
        request.user = self.user.user
        response = new_booking(request)
        self.assertEqual(response.status_code, 200)

    def test_get_request_anonymous(self):
        url = '/booking/newbooking/'
        response = self.client.get(url, follow=True)
        self.assertTemplateUsed(response, 'sas/index.html')

    def test_post_not_valid(self):
        start_date = datetime.strptime("21091999", "%d%m%Y")
        parameters = {
            'name': 'Reservaoiasd', 'start_hour': self.hour,
            'end_hour': self.hour2, 'start_date': start_date,
            'end_date': self.end_date, 'building': self.building_name,
            'place': self.place_name, 'week_days': self.week_days}

        request = self.factory.get('/booking/newbooking/', follow=True)
        client = self.client
        username = self.user.user.username
        client.login(username=username, password='1234567')
        response = client.post('/booking/newbooking/', parameters)
        self.assertTemplateUsed(response, 'booking/newBooking.html')
        self.assertContains(response, 'Inputs are invalid')

    def test_form_is_valid(self):
        form = BookingForm(data=self.parameters)
        self.assertTrue(form.is_valid())


class TestBookTime(TestCase):

    def test_get_str_weekday(self):
        book = BookTime()
        book.date_booking = datetime.strptime("21092016", "%d%m%Y")
        self.assertEqual(book.get_str_weekday(), "Wednesday")

    def test_get_str_weekday(self):
        book = BookTime()
        book.date_booking = datetime.strptime("21092016", "%d%m%Y")
        self.assertEqual(book.get_str_weekday(), "Wednesday")


class TestSearchBooking(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_get_str_weekday(self):
        book = BookTime()
        book.date_booking = datetime.strptime("21092016", "%d%m%Y")
        self.assertEqual(book.get_str_weekday(), "Wednesday")

    def test_search_booking_booking_name_week(self):
        factory = self.factory
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=7)
        booking_name = Booking.objects.get(name='PI 1 - Projeto Integrador 1')

        parameters = {'search_options': 'opt_booking_week',
                      'booking_name': booking_name,
                      'start_date': start_date,
                      'end_date': end_date}

        form = SearchBookingForm(data=parameters)

        form.is_valid()
        request = factory.post('/booking/searchbookingg', parameters)
        page = search_booking_booking_name_week(request=request,
                                                form_booking=form)
        self.assertEqual(page.status_code, 200)
        self.assertContains(page, 'Booking x Week')

    def test_search_booking_post_not_valid(self):
        client = self.client
        start_date = datetime.now().date() - timedelta(days=6)
        building_name = Building.objects.filter(name='UAC')
        room_name = Place.objects.filter(pk=8)
        parameters = {
            'search_options': 'opt_day_room',
            'building_name': building_name,
            'room_name': room_name, 'start_date': start_date}
        response = client.post('/booking/searchbookingg/', parameters)
        self.assertTemplateUsed(response, 'booking/searchBookingQuery.html')


class TestSearchBookingQuery(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_count_days(self):
        form = SearchBookingForm()
        start_date = datetime.strptime("21092016", "%d%m%Y")
        end_date = datetime.strptime("22092016", "%d%m%Y")
        days = [start_date, end_date]
        days2 = form.count_days(start_date=start_date, end_date=end_date)
        self.assertEqual(days, days2)

    def test_search_booking_day_room(self):
        factory = self.factory
        start_date = datetime.now().date()
        building_name = Building.objects.filter(name='UAC')
        room_name = Place.objects.filter(pk=8)
        parameters = {'search_options': 'opt_day_room',
                      'building_name': building_name,
                      'room_name': room_name,
                      'start_date': start_date}
        form = SearchBookingForm(data=parameters)
        form.is_valid()
        request = factory.post('/booking/searchbookingg', parameters)
        page = search_booking_day_room(request=request, form_booking=form)
        self.assertEqual(page.status_code, 200)
        self.assertContains(page, "Room x Day")

    def test_search_booking_booking_name_week(self):
        factory = self.factory
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=7)
        booking_name = Booking.objects.get(name='PI 1 - Projeto Integrador 1')

        parameters = {'search_options': 'opt_booking_week',
                      'booking_name': booking_name,
                      'start_date': start_date,
                      'end_date': end_date}

        form = SearchBookingForm(data=parameters)

        form.is_valid()
        request = factory.post('/booking/searchbookingg', parameters)
        page = search_booking_booking_name_week(request=request,
                                                form_booking=form)
        self.assertEqual(page.status_code, 200)
        self.assertContains(page, 'Booking x Week')

    def test_form_is_valid(self):
        start_date = datetime.now().date()
        building_name = Building.objects.filter(name='UAC')
        room_name = Place.objects.filter(pk=8)
        parameters = {'search_options': 'opt_day_room',
                      'building_name': building_name,
                      'room_name': room_name,
                      'start_date': start_date}
        form = SearchBookingForm(data=parameters)
        self.assertTrue(form.is_valid())

    def test_days_list(self):
        start_date = datetime.strptime("21092017", "%d%m%Y")
        end_date = datetime.strptime("22092017", "%d%m%Y")
        building_name = Building.objects.get(name='UAC')
        room_name = Place.objects.get(pk=9)
        parameters = {'search_options': 'opt_room_period',
                      'building_name': building_name,
                      'room_name': room_name,
                      'start_date': start_date,
                      'end_date': end_date}
        form = SearchBookingForm(data=parameters)
        form.is_valid()
        days = []
        days.append(start_date.date())
        days.append(end_date.date())
        days2 = form.days_list()
        self.assertEqual(days, days2)

    def test_search_booking_room_period(self):
        factory = self.factory
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=50)
        building_name = Building.objects.filter(name='UAC')
        room_name = Place.objects.filter(pk=8)
        parameters = {'search_options': 'opt_room_period',
                      'building_name': building_name,
                      'room_name': room_name,
                      'start_date': start_date,
                      'end_date': end_date}
        form = SearchBookingForm(data=parameters)
        form.is_valid()
        request = factory.post('/booking/searchbookingg', parameters)
        page = search_booking_room_period(request=request, form_booking=form)
        self.assertEqual(page.status_code, 200)
        self.assertContains(page, "Room x Period")
        parameters = {'search_options': 'opt_day_room',
                      'building_name': building_name,
                      'room_name': room_name,
                      'start_date': start_date}

        form = SearchBookingForm(data=parameters)
        self.assertTrue(form.is_valid())


class TestSearchBookingForm(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_day(self):
        start_date = datetime.strptime("12/31/2016", "%m/%d/%Y")
        parameters = {'start_date': start_date}
        booking = SearchBookingForm(data=parameters)
        if booking.is_valid():
            aux = booking.get_day()
            self.assertEqual(start_date, day)

    def test_search_booking_post_not_valid(self):
        client = self.client
        start_date = datetime.now().date() - timedelta(days=6)
        building_name = Building.objects.filter(name='UAC')
        room_name = Place.objects.filter(pk=8)
        parameters = {'search_options': 'opt_day_room',
                      'building_name': building_name,
                      'room_name': room_name,
                      'start_date': start_date}
        response = client.post('/booking/searchbookingg/', parameters)
        self.assertTemplateUsed(response, 'booking/searchBookingQuery.html')

    def test_search_booking_building_day(self):
        factory = RequestFactory()
        start_date = datetime.now().date()
        building_name = Building.objects.filter(name='UAC')
        parameters = {'search_options': 'opt_building_day',
                      'building_name': building_name,
                      'start_date': start_date}
        form = SearchBookingForm(data=parameters)
        form.is_valid()
        request = factory.post('/booking/searchbookingg/', parameters)
        page = search_booking_building_day(request=request, form_booking=form)
        self.assertEqual(page.status_code, 200)
        self.assertContains(page, 'Building x Day')
