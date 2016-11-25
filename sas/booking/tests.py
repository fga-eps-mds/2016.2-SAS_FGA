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
from booking.views import search_booking_responsible
from booking.urls import *
from user.models import UserProfile, Settings
from booking.models import Booking
from booking.forms import BookingForm, SearchBookingForm
from dateutil import parser
from booking.views import search_booking_room_period
from django.db.models import Q
from booking.factories import BookTimeFactory, BookingFactory
from booking.views import approve_booking
from booking.views import deny_booking
from booking.templatetags.check_table import search_building
from booking.templatetags.check_table import search_place, search_hour
from booking.templatetags.check_table import search_user, aux_search_date
from booking.templatetags.check_table import search_date, search_tags
from booking.templatetags.booking_handling import is_all_bookings
from booking.templatetags.booking_handling import status_glyphicon


class DeleteBookingTest(TestCase):

    def setUp(self):
        self.user = UserProfileFactory.create()
        self.user.user.set_password('1234567')
        self.user.save()
        self.booking = BookingFactory.create(user=self.user.user)
        self.booking.save()
        self.client = Client()

    def test_admin_delete_booking(self):
        self.user.make_as_admin()
        self.user.save()
        self.client.login(username=self.user.user.username,
                          password='1234567')
        url = reverse('booking:deletebooking', args=(self.booking.id,))
        response = self.client.get(url)
        self.assertFalse(Booking.objects.filter(pk=self.booking.id).exists())
        self.assertContains(response, 'Booking deleted!')

    def test_academic_staff_delete_their_own_booking(self):
        self.user.make_as_academic_staff()
        self.user.save()
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
        self.booking = BookingFactory(user=self.user.user)
        print(self.booking)
        print(self.booking.time.all())
        self.client = Client()
        self.id_booking = self.booking.id
        self.id_booktime = self.booking.time.all()[0].id

    def test_admin_delete_booktime(self):
        self.user.make_as_admin()
        self.user.save()
        self.client.login(username=self.user.user.username,
                          password='1234567')
        url = reverse('booking:deletebooktime',
                      args=[self.id_booking, self.id_booktime])
        response = self.client.get(url)
        self.assertFalse(BookTime.objects.filter(
            pk=self.id_booktime).exists())
        self.assertContains(response, 'Booking deleted!')

    def test_academic_staff_delete_their_own_booktime(self):
        self.user.make_as_academic_staff()
        self.client.login(username=self.user.user.username,
                          password='1234567')
        url = reverse('booking:deletebooktime',
                      args=[self.id_booking, self.id_booktime])
        response = self.client.get(url)
        self.assertFalse(BookTime.objects.filter(pk=self.id_booktime).exists())
        self.assertContains(response, 'Booking deleted!')

    def test_doesnt_have_permission(self):
        self.user.make_as_academic_staff()
        self.user.save()
        booking = BookingFactory.create()
        self.client.login(username=self.user.user.username, password='1234567')
        url = reverse('booking:deletebooktime',
                      args=[booking.id, booking.time.all()[0].id])
        response = self.client.get(url)
        self.assertContains(response, 'You cannot delete this booking.')

    def test_user_not_logged_in(self):
        url = reverse('booking:deletebooktime',
                      args=[self.id_booking, self.id_booktime])
        response = self.client.get(url)
        self.assertTrue(BookTime.objects.filter(
            pk=self.id_booktime).exists())
        self.assertTrue(Booking.objects.filter(
            pk=self.id_booking).exists())

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
        self.semester = Settings()
        self.semester.start_semester = datetime.strptime("21092017", "%d%m%Y")
        self.semester.end_semester = datetime.strptime("22092018", "%d%m%Y")
        self.semester.save()
        self.client = Client()
        self.factory = RequestFactory()
        self.week_days = ['3', '5']
        self.start_date = datetime.strptime("21092017", "%d%m%Y").date()
        self.end_date = datetime.strptime("22102017", "%d%m%Y").date()
        self.hour = datetime.strptime("08:00", "%H:%M").time()
        self.hour2 = datetime.strptime("10:00", "%H:%M").time()
        self.building_name = Building.objects.filter(name='UAC')
        self.place_name = Place.objects.filter(pk=3)
        self.parameters = {
            'name': 'Reservaoiasd', 'start_hour': self.hour,
            'end_hour': self.hour2, 'start_date': self.start_date,
            'end_date': self.end_date, 'building': self.building_name[0].pk,
            'place': self.place_name[0].pk, 'week_days': self.week_days,
            'date_options': 'opt_select_date', 'tags': 'hello'}

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

    def test_responsible(self):
        username = self.user.user.username
        client = self.client
        self.user.make_as_admin()
        responsible_user = UserProfileFactory.create()
        self.parameters['date_options'] = 'opt_select_date'
        self.parameters['engineering_choice'] = '1'
        self.parameters['responsible'] = responsible_user.__str__()
        client.login(username=username, password='1234567')
        response = client.post('/booking/newbooking/', self.parameters)
        booking = Booking.objects.get(name=self.parameters['name'])
        self.assertEqual(booking.user.id, responsible_user.user.id)

    def test_responsible_not_an_user(self):
        username = self.user.user.username
        client = self.client
        self.user.make_as_admin()
        self.parameters['date_options'] = 'opt_select_date'
        self.parameters['engineering_choice'] = '1'
        self.parameters['responsible'] = 'Carla Rocha'
        client.login(username=username, password='1234567')
        response = client.post('/booking/newbooking/', self.parameters)
        booking = Booking.objects.get(name=self.parameters['name'])
        self.assertEqual(booking.user.id, self.user.user.id)
        self.assertEqual(booking.responsible, self.parameters['responsible'])


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
        self.assertContains(page, 'Booking')

    def test_search_booking_responsible(self):
        factory = self.factory
        date = datetime.strptime("22112016", "%d%m%Y")
        booking_responsible = 'rocha.carla@gmail.com'

        parameters = {'search_options': 'opt_responsible',
                      'responsible': booking_responsible,
                      'start_date': date}

        form = SearchBookingForm(data=parameters)

        form.is_valid()
        request = factory.post('/booking/searchbookingg', parameters)
        page = search_booking_responsible(request=request,
                                          form_booking=form)
        self.assertEqual(page.status_code, 200)
        self.assertContains(page, 'Responsible')

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
        self.assertContains(page, "Timetable")

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
        self.assertContains(page, 'Booking')

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
        user = UserProfileFactory.create()
        booking = BookingFactory.create(user=user.user, start_date=start_date,
                                        end_date=end_date)
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
        self.assertContains(page, "Room")
        parameters = {'search_options': 'opt_day_room',
                      'building_name': building_name,
                      'room_name': room_name,
                      'start_date': start_date}

        form = SearchBookingForm(data=parameters)
        self.assertTrue(form.is_valid())

    def test_get_str_weekday(self):
        book = BookTime()
        book.date_booking = datetime.strptime("21092016", "%d%m%Y")
        self.assertEqual(book.get_str_weekday(), "Wednesday")


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
        self.assertContains(page, 'Occupation')


class BookingTest(TestCase):
    def setup(self):
        self.booking = Booking()
        self.place = Place()

    def test_get_bookings(self):
        self.booking = Booking.objects.order_by('name').first()
        result = Booking.get_bookings()
        self.assertEqual(result[0][0], self.booking.name)

    def test_get_responsibles(self):
        result = Booking.get_responsibles()
        self.booking = Booking.objects.first()
        self.assertEqual(result[1][1], self.booking.responsible)

    def test_get_places(self):
        self.booking = Booking.objects.all()
        self.place = Place.objects.get(id=8)
        result_place, result_place_name = Booking.get_places(self.booking)
        place_name = self.place.name.split('-')
        self.assertEqual(result_place[0], self.place)
        self.assertEqual(result_place_name[0], place_name[1])


class ValidationTest(TestCase):
    def setUp(self):
        self.validation = Validation()

    # True validations
    def test_has_numbers(self):
        self.assertEqual(self.validation.hasNumbers('Test123'), True)

    def test_has_letters(self):
        self.assertEqual(self.validation.hasLetters('123Test'), True)

    def test_has_special_characters(self):
        self.assertEqual(self.validation.hasSpecialCharacters('#Test'), True)

    # False validations
    def test_has_no_numbers(self):
        self.assertEqual(self.validation.hasNumbers('Test Test'), None)

    def test_has_no_letters(self):
        self.assertEqual(self.validation.hasLetters('123456'), None)

    def test_has_no_special_characters(self):
        self.assertEqual(self.validation.hasSpecialCharacters('Other'), None)


class BuildingTest(TestCase):

    def setUp(self):
        self.building = Building()

    def test_set_name(self):
        name = "Minhocão"
        self.building.name = name
        name_size = len(name)
        building_name_size = len(self.building.name)
        self.assertEqual(building_name_size, name_size)

    def test_str(self):
        self.building.name = "Minhocão"
        self.assertEqual(self.building.__str__(), "Minhocão")


class PlaceTest(TestCase):

    def setUp(self):
        self.place = Place()

    def test_set_name(self):
        self.place.name = "Sala 2"
        self.assertEqual(self.place.__str__(), "Sala 2")


class BookingTimeTest(TestCase):

    def setUp(self):
        self.bookingtime = BookTimeFactory.create()

    def test_add_days(self):
        booking_time_add = self.bookingtime.date_booking + timedelta(days=1)
        self.bookingtime.add_days(1)
        self.assertEqual(self.bookingtime.date_booking, booking_time_add)

    def test_range_days(self):
        booking2 = self.bookingtime.date_booking
        self.bookingtime.add_days(1)
        booking1 = self.bookingtime.date_booking
        date_ranges = date_range(booking2, booking1)
        self.assertEqual(len(date_ranges), 2)

    def test_next_week_day_with_diff_more_than_zero(self):
        date_booking = self.bookingtime.date_booking + timedelta(days=6)
        nr_weekday = self.bookingtime.date_booking.weekday() - 1
        self.bookingtime.next_week_day(nr_weekday=nr_weekday)
        self.assertEqual(date_booking, self.bookingtime.date_booking)

    def test_next_week_day_with_diff_less_than_zero(self):
        date_booking = self.bookingtime.date_booking + timedelta(days=1)
        nr_weekday = self.bookingtime.date_booking.weekday() + 1
        self.bookingtime.next_week_day(nr_weekday=nr_weekday)
        self.assertEqual(date_booking, self.bookingtime.date_booking)

    def test_next_week_day_with_diff_equals_zero(self):
        date_booking = self.bookingtime.date_booking + timedelta(days=7)
        nr_weekday = self.bookingtime.date_booking.weekday()
        self.bookingtime.next_week_day(nr_weekday=nr_weekday)
        self.assertEqual(date_booking, self.bookingtime.date_booking)

    def test_get_str_weekday(self):
        book = BookTime()
        book.date_booking = datetime.strptime("21092016", "%d%m%Y")
        self.assertEqual(book.get_str_weekday(), "Wednesday")


class PendingBookingTest(TestCase):
    def setUp(self):
        self.booking = BookingFactory.create()
        self.booking.place.is_laboratory = True
        self.booking.save()
        self.factory = RequestFactory()
        self.userprofile = UserProfileFactory.create()
        self.userprofile.make_as_admin()
        self.userprofile.user.set_password('123456')
        self.userprofile.save()
        self.client = Client()
        self.username = self.userprofile.user.username

    def test_update_status(self):
        self.booking.update_status(status=0)
        status = self.booking.status
        self.assertEqual(status, 0)

    def test_approve_booking(self):
        self.client.login(username=self.username,
                          password='123456')
        url = reverse('booking:approvebooking', args=(self.booking.id,))
        response = self.client.get(url)
        self.assertContains(response, 'Booking Approved!')

    def test_view_approve_invalid_booking(self):
        pk = self.booking.pk + 10000
        self.client.login(username=self.username, password='123456')
        url = reverse('booking:approvebooking', args=(pk,))
        response = self.client.get(url)
        self.assertContains(response, 'Booking not found.')

    def test_view_deny_booking(self):
        pk = self.booking.pk
        self.client.login(username=self.username, password='123456')
        url = reverse('booking:denybooking', args=(pk,))
        response = self.client.get(url)
        self.assertContains(response, 'Booking Denied!')

    def test_view_deny_invalid_booking(self):
        pk = self.booking.pk + 10000
        self.client.login(username=self.username, password='123456')
        url = reverse('booking:denybooking', args=(pk,))
        response = self.client.get(url)
        self.assertContains(response, 'Booking not found.')


class CheckTableTest(TestCase):
    def setUp(self):
        self.place = Place.objects.all()
        self.start_hour = timedelta(hours=6)
        self.end_hour = timedelta(hours=8)
        self.midnight = timedelta(hours=0)
        self.date = datetime.strptime('Jun 1 2025', '%b %d %Y')

    def test_search_building_query(self):
        place = self.place
        result = search_building(place, 30)

        self.assertEquals(result, '2')

    def test_search_building_obj(self):
        place = self.place.get(pk=1)
        result = search_building(place, 1)
        self.assertEquals(result, '1')

    def test_search_place_query(self):
        place = self.place
        result = search_place(place, 10)
        self.assertEquals(result, '11')

    def test_search_place_obj(self):
        place = self.place.get(pk=20)
        result = search_place(place, 1)
        self.assertEquals(result, '20')

    def test_search_hour_start_hour(self):
        result = search_hour(6, 0)
        self.assertEquals(result, self.start_hour)

    def test_search_hour_end_hour(self):
        result = search_hour(6, 1)
        self.assertEquals(result, self.end_hour)

    def test_search_hour_midnight(self):
        result = search_hour(22, 1)
        self.assertEquals(result, self.midnight)

    def test_search_date_obj(self):
        date = self.date, 7
        result = search_date(date, 1)
        self.assertEquals(result, str(self.date))

    def test_search_date_list(self):
        dates = []
        dates.append(self.date)
        dates.append(self.date)
        date = dates, 7
        result = search_date(dates, 1)
        self.assertEquals(result, str(self.date))


class ShowBookTimesTest(TestCase):
    def setUp(self):
        self.user = UserProfileFactory.create()
        self.user.user.set_password('1234567')
        self.user.save()
        self.client = Client()

    def test_booking_not_found(self):
        self.user.make_as_admin()
        self.user.save()
        self.client.login(username=self.user.user.username, password='1234567')
        url = reverse('booking:showbooktimes', args=(0,))
        response = self.client.get(url)
        self.assertContains(response, 'Booking not found.')


class TemplateTagsTest(TestCase):
    def test_is_all_bookings(self):
        name = 'All Bookings'
        result = is_all_bookings(name)
        self.assertTrue(result)

    def test_search_user(self):
        users = UserProfile.get_users()
        self.assertEquals(search_user(), users)

    def test_aux_search_date(self):
        days_n = (7, 8)
        self.assertEquals(aux_search_date(7, 8), days_n)

    def test_status_glyphicon(self):
        nothing = 0
        self.assertEqual(status_glyphicon(nothing), None)

    def test_search_place(self):
        places_list = list(Place.objects.all())
        pk = str(places_list[0].pk)
        self.assertEqual(search_place(places_list, 0), pk)

    def test_search_building(self):
        places_list = list(Place.objects.all())
        pk = str(places_list[0].building.pk)
        self.assertEqual(search_building(places_list, 0), pk)



class TestBookingTags(TestCase):
    def setUp(self):
        self.booking = BookingFactory.create()
        self.booking.place.is_laboratory = True
        self.booking.save()
        self.tag = Tag(name="teste")
        self.tag.save()
        self.tag2 = Tag(name="teste2")
        self.tag2.save()
        self.user = UserProfileFactory.create()
        self.user.user.set_password('1234567')
        self.user.save()
        self.client = Client()
        self.booking.tags.add(self.tag)
        self.booking.save()

    def test_booking_details_not_found_admin(self):
        self.user.make_as_admin()
        self.user.save()
        self.client.login(username=self.user.user.username, password='1234567')
        url = reverse('booking:bookingdetails', args=(0,))
        response = self.client.get(url)
        self.assertContains(response, 'Booking not found.')

    def test_booking_details_not_found_user(self):
        self.client.login(username=self.user.user.username, password='1234567')
        url = reverse('booking:bookingdetails', args=(0,))
        response = self.client.get(url)
        self.assertContains(response, 'Booking not found.')

    def test_booking_details_found(self):
        self.client.login(username=self.user.user.username, password='1234567')
        url = reverse('booking:bookingdetails', args=(self.booking.pk,))
        response = self.client.get(url)
        self.assertContains(response, self.booking.name)

    def test_tagged_bookings_found(self):
        self.client.login(username=self.user.user.username, password='1234567')
        url = reverse('booking:taggedbookings', args=(self.tag.pk,))
        response = self.client.get(url)
        self.assertContains(response, self.booking.name)

    def test_tagged_bookings_not_found(self):
        self.client.login(username=self.user.user.username, password='1234567')
        url = reverse('booking:taggedbookings', args=(self.tag2.pk,))
        response = self.client.get(url, follow=True)
        self.assertContains(response, "Booking not found.")

    def test_get_tags(self):
        self.assertEquals(Tag.get_tags()[1][0], self.tag)

    def test_search_tags_tag(self):
        self.assertEquals(search_tags()[1][0], self.tag)

    def test_print_tags(self):
        self.assertEquals("teste", self.tag.__str__())
