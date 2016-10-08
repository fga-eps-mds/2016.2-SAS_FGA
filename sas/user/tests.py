from django.test import TestCase, RequestFactory
from user.models import *
from django.test import Client
from django.contrib.auth.models import AnonymousUser
from user.views import delete_user
from user.factories import UserProfileFactory
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class DeleteUserTest(TestCase):
	def setUp(self):
		self.userprofile = UserProfile()
		self.userprofile.name("Gustavo Rodrigues Coelho")
		self.userprofile.registration_number = "110030559"
		self.userprofile.category = 'Student'
		self.userprofile.user.username = "gutorc@hotmail.com"
		self.userprofile.user.email = "gutorc@hotmail.com"
		self.userprofile.user.set_password('123456')
		self.userprofile.save()
		self.client = Client()
		self.factory = RequestFactory()
		self.url = '/user/delete/'

	def test_get_request_logged(self):
		client = self.client
		client.login(username='gutorc@hotmail.com', password='123456')
		response = self.client.get(self.url, follow = True)
		self.assertTemplateUsed(response, 'sas/index.html')
		self.assertEqual(response.status_code, 200)


	def test_get_request_anonymous(self):
		response = self.client.get(self.url, follow = True)
		self.assertTemplateUsed(response, 'sas/index.html')
		self.assertEqual(response.status_code, 200)

	def test_delete_user(self):
		userprofile = self.userprofile
		client = self.client
		client.login(username='gutorc@hotmail.com', password='123456')
		response = self.client.get(self.url, follow = True)
		self.assertEqual(False,UserProfile.objects.filter(registration_number="110030559").exists())


class ViewsTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_index(self):
        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)

    def test_new_user(self):
        result = self.client.get("/user/newuser/")
        self.assertEqual(result.status_code, 200)


class UserProfileTest(TestCase):

    def setUp(self):
        self.userprofile = UserProfile()

    def test_set_name(self):
        self.userprofile.name("Gustavo Rodrigues Coelho")
        self.assertEqual(self.userprofile.user.first_name, "Gustavo")
        self.assertEqual(self.userprofile.user.last_name, "Rodrigues Coelho")

    def test_get_full_name(self):
        name = "Pedro Pereira Pinto"
        self.userprofile.name(name)
        self.assertEqual(self.userprofile.full_name(), name)

    def test_category(self):
        self.assertEqual(len(CATEGORY), 4)

    def test_save(self):
        self.userprofile.name("Gustavo Rodrigues Coelho")
        self.userprofile.registration_number = "11/0030559"
        self.userprofile.user.username = "gutorc@hotmail.com"
        self.userprofile.user.email = "gutorc@hotmail.com"
        self.userprofile.save()
        self.assertEqual(self.userprofile.pk, 1)


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
        self.assertEqual(self.validation.hasNumbers('Test Test'), False)

    def test_has_no_letters(self):
        self.assertEqual(self.validation.hasLetters('123456'), False)

    def test_has_no_special_characters(self):
        self.assertEqual(self.validation.hasSpecialCharacters('Other'), False)

    # Empty Validations
    def test_has_numbers_empty(self):
        self.assertEqual(self.validation.hasNumbers(''), False)

    def test_has_letters_empty(self):
        self.assertEqual(self.validation.hasLetters(''), False)

    def test_has_special_characters_empty(self):
        self.assertEqual(self.validation.hasSpecialCharacters(''), False)

    # None Validations
    def test_has_numbers_none(self):
        self.assertEqual(self.validation.hasNumbers(None), False)

    def test_has_letters_none(self):
        self.assertEqual(self.validation.hasLetters(None), False)

    def test_has_special_characters_none(self):
        self.assertEqual(self.validation.hasSpecialCharacters(None), False)
