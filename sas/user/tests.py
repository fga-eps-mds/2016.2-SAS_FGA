from django.test import TestCase
from user.models import *
from django.test import Client
from user.factories import UserFactory


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

class LoginTest(TestCase):
	def setUp(self):
		self.user = UserFactory.create()
		self.user.set_password('1234')
		self.client = Client()

	def test_get_request(self):
		response = self.client.get('/user/login/', follow = True)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.redirect_chain, [('/', 302)])

	def test_invalid_email(self):
		response = self.client.post('/user/login/', {'email' : 'aeiou', 'password' : '123'})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Informe um endereço de email válido.')

	def test_invalid_password(self):
		response = self.client.post('/user/login/', {'email' : self.user.email, 'password' : '123'})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Email or Password does not match')
