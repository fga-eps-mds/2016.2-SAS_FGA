from django.test import TestCase, RequestFactory
from user.models import *
from django.test import Client
from django.contrib.auth.models import AnonymousUser
from user.views import delete_user
from user.factories import UserProfileFactory


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
		client = self.client
		client.login(username='gutorc@hotmail.com', password='123456')
		response = self.client.get(self.url, follow = True)
		self.assertRaises(self.userprofile, None)


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
