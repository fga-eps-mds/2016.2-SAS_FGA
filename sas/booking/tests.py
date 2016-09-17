from django.test import TestCase
from booking.models import *

class UserProfileTest(TestCase):
	
	def setUp(self):
		self.userprofile = UserProfile()
		self.userprofile.user = User()

	def test_set_name(self):
		self.userprofile.name("Gustavo Rodrigues Coelho")
		self.assertEqual(self.userprofile.user.first_name,"Gustavo")
		self.assertEqual(self.userprofile.user.last_name,"Rodrigues Coelho")

	def test_get_full_name(self):
		name = "Pedro Pereira Pinto"
		self.userprofile.name(name)
		self.assertEqual(self.userprofile.full_name(),name)

	def test_category(self):
		self.assertEqual(len(CATEGORY),3)		

