from django.test import TestCase
from booking.models import UserProfile
from booking.views import edit_user,delete_user

class DeleteUserTestCase(TestCase):

    user_profile = UserProfile()
    user_profile.name = 'Teste'
    user_profile.category = 'Aluno'
    user_profile.registration_number = 10;
    user_profile.email = 'example@example.com'
    id_test = user_profile.id

    def setUp(self):
        self.delete_user = delete_user()
    def delete_confirmed(self):
        self.assertEqual(delete_user(request.POST['delete'],id_test), render(request, 'booking/index.html',{}))
    def delete_cancelled(self):
        self.assertEqual(delete_user(request.POST['cancel'],id_test), render(request,'booking/listUser.html',user_profile))

class EditUserTestCase(TestCase):
		user_profile = UserProfile()
		user_profile.registration_number = 3
		user_profile.category='Aluno'
		user_profile.name='Testing'
		user_profile.username='testing1'
		user_profile.email='example@example.com'				
		user_id = user_profile.id

	def setUp(self):
		self.edit_user = edit_user()

	def test_edit_user_success(self):
		self.assertEqual(edit_user(request.POST['edituser'],user_id), render(request, 'booking/index.html',{}))
