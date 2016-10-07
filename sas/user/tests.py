from django.test import TestCase
from user.models import *
from django.test import Client


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
		self.assertEqual(self.validation.hasNumbers('Test123'), True);

	def test_has_letters(self):
		self.assertEqual(self.validation.hasLetters('123Test'), True);

	def test_has_special_characters(self):
		self.assertEqual(self.validation.hasSpecialCharacters('#Test'), True);

	# False validations
	def test_has_no_numbers(self):
		self.assertEqual(self.validation.hasNumbers('Test Test'), False);

	def test_has_no_letters(self):
		self.assertEqual(self.validation.hasLetters('123456'), False);

	def test_has_no_special_characters(self):
		self.assertEqual(self.validation.hasSpecialCharacters('Another Test'), False);
