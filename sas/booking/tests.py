from django.test import TestCase
from .views import delete_user
from .models import UserProfile

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
