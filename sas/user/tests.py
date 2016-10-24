from django.test import TestCase, RequestFactory
from user.models import UserProfile, Validation, CATEGORY
from django.test import Client
from user.views import edit_user
from user.factories import UserProfileFactory
from django.contrib.auth import logout
from django.urls import reverse


class EditUserTest(TestCase):
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

    def test_get_request_logged(self):
        request = self.factory.get('/user/edituser/')
        request.user = self.userprofile.user
        response = edit_user(request)
        self.assertEqual(response.status_code, 200)

    def test_get_request_anonymous(self):
        url = '/user/edituser/'
        response = self.client.get(url, follow=True)
        self.assertTemplateUsed(response, 'sas/index.html')

    def test_edit_post_registration_number(self):
        self.factory.get('/user/edituser/')
        client = self.client
        client.login(username='gutorc@hotmail.com', password='123456')
        parameters = {'name': 'Pedro', 'registration_number': '140000000',
                      'category': '1', 'email': "gutorc@hotmail.com"}
        client.post('/user/edituser/', parameters)
        self.userprofile.refresh_from_db()
        self.assertEqual('140000000', self.userprofile.registration_number)


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
        response = self.client.get(self.url, follow=True)
        self.assertTemplateUsed(response, 'sas/index.html')
        self.assertEqual(response.status_code, 200)

    def test_get_request_anonymous(self):
        response = self.client.get(self.url, follow=True)
        self.assertTemplateUsed(response, 'sas/index.html')
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        client = self.client
        client.login(username='gutorc@hotmail.com', password='123456')
        self.client.get(self.url, follow=True)
        self.assertEqual(False,
                         UserProfile.objects.filter(registration_number="110030559").exists())


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
        self.userprofile.name("Pedro Pereira Pinto")
        self.assertEqual(self.userprofile.user.first_name, "Pedro")
        self.assertEqual(self.userprofile.user.last_name, "Pereira Pinto")

    def test_create_user(self):
        self.assertFalse(hasattr(self.userprofile, 'user'))
        self.userprofile.create_user()
        self.assertTrue(hasattr(self.userprofile, 'user'))

    def test_get_full_name(self):
        name = "Pedro Pereira Pinto"
        self.userprofile.name(name)
        self.assertEqual(self.userprofile.full_name(), name)
        name = "Renan Calheiros"
        self.userprofile.name(name)
        self.assertEqual(self.userprofile.full_name(), name)

    def test_category(self):
        self.assertEqual(len(CATEGORY), 4)

    def test_registration_number(self):
        registration_number = "123456789"
        self.userprofile.registration_number = registration_number
        registration_size = len(registration_number)
        profile_registration_size = len(self.userprofile.registration_number)
        self.assertEqual(profile_registration_size, registration_size)

    def test_registration_number_bigger(self):
        registration_number = "0123456789"
        self.userprofile.registration_number = registration_number
        registration_size = len(registration_number)
        self.assertGreater(registration_size, 9)

    def test_registration_number_smaller(self):
        registration_number = "01234567"
        self.userprofile.registration_number = registration_number
        registration_size = len(registration_number)
        self.assertLess(registration_size, 9)

    def test_save(self):
        self.userprofile.name("Gustavo Rodrigues Coelho")
        self.userprofile.registration_number = "11/0030559"
        self.userprofile.user.username = "gutorc@hotmail.com"
        self.userprofile.user.email = "gutorc@hotmail.com"
        self.userprofile.save()
        self.assertEqual(self.userprofile.pk, 3)

    def test_is_admin(self):
        userprofile = UserProfileFactory.create()
        self.assertFalse(userprofile.is_admin())
        userprofile.make_as_admin()
        self.assertTrue(userprofile.is_admin())

    def test_is_academic_staff(self):
        userprofile = UserProfileFactory.create()
        self.assertFalse(userprofile.is_academic_staff())
        userprofile.make_as_academic_staff()
        self.assertTrue(userprofile.is_academic_staff())


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


class LoginTest(TestCase):
    def setUp(self):
        self.user = UserProfileFactory.create()
        self.user.user.set_password('1234567')
        self.user.save()
        self.client = Client()

    def test_get_request(self):
        response = self.client.get('/user/login/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain, [('/', 302)])

    def test_invalid_email(self):
        response = self.client.post('/user/login/', {'email': 'aeiou',
                                                     'password': '1234567'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter a valid email address.')

    def test_invalid_password(self):
        response = self.client.post('/user/login/',
                                    {'email': self.user.user.email,
                                     'password': '1235567'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Email or Password does not match')

    def test_valid_user(self):
        logout(self.client)
        response = self.client.post('/user/login/',
                                    {'email': self.user.user.email,
                                     'password': '1234567'},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain, [('/', 302)])
        self.assertContains(response, 'Hi, %s' % (self.user.full_name()))


class LogoutTest(TestCase):
    def setUp(self):
        self.user = UserProfileFactory.create()
        self.user.user.set_password('1234567')
        self.user.save()
        self.client = Client()

    def test_logout(self):
        self.client.login(username=self.user.user.email, password='1234567')
        response = self.client.get('/user/logout/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain, [('/', 302)])
        self.assertContains(response, 'You have been logged out successfully!')

    def test_invalid_logout(self):
        response = self.client.get('/user/logout/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain, [('/', 302)])
        self.assertNotContains(response,
                               'You have been logged out sucessfully!')


class AdminSearchUserTest(TestCase):
    def setUp(self):
        self.admin = UserProfileFactory.create()
        self.admin.user.set_password('1234567')
        self.admin.make_as_admin()
        self.admin.save()
        self.client = Client()
        self.users = [UserProfileFactory.create() for x in range(5)]
        for user in self.users:
            user.make_as_academic_staff()

    def test_search_users(self):
        self.client.login(username=self.admin.user.username,
                          password='1234567')
        response = self.client.get(reverse('user:searchuser'))
        for user in self.users:
            self.assertContains(response, user.full_name())
            self.assertContains(response, user.registration_number)

    def test_user_doesnt_have_permission(self):
        self.users[0].user.set_password('1234567')
        self.users[0].save()
        self.client.login(username=self.users[0].user.username,
                          password='1234567')
        response = self.client.get(reverse('user:searchuser'), follow=True)
        self.assertContains(response, 'You cannot access this page.')

    def test_user_not_logged_in(self):
        response = self.client.get(reverse('user:searchuser'), follow=True)
        self.assertNotContains(response, 'Make an Admin')

        
class MakeUserAnAdminTest(TestCase):

    def setUp(self):
        self.admin = UserProfileFactory.create()
        self.admin.user.set_password('1234567')
        self.admin.make_as_admin()
        self.admin.save()
        self.user = UserProfileFactory.create()
        self.client = Client()

    def test_academic_staff_to_admin(self):
        self.client.login(username=self.admin.user.username,
                          password='1234567')
        self.user.make_as_academic_staff()
        url = reverse('user:usertoadmin', args=(self.user.id,))
        response = self.client.get(url)
        self.assertContains(response, 'User ' + self.user.full_name() +
                            ' is now an admin.')
        self.assertFalse(self.user.is_academic_staff())
        self.assertTrue(self.user.is_admin())

    def test_user_is_already_admin(self):
        self.client.login(username=self.admin.user.username,
                          password='1234567')
        self.user.make_as_admin()
        url = reverse('user:usertoadmin', args=(self.user.id,))
        response = self.client.get(url)
        self.assertContains(response, 'User ' + self.user.full_name() +
                            ' is already an admin.')
        self.assertFalse(self.user.is_academic_staff())
        self.assertTrue(self.user.is_admin())

    def test_user_does_not_exist(self):
        self.client.login(username=self.admin.user.username,
                          password='1234567')
        url = reverse('user:usertoadmin', args=(9999,))
        response = self.client.get(url)
        self.assertContains(response, 'User not found.')

    def test_user_doesnt_have_permission(self):
        self.admin.user.groups.clear()
        self.admin.make_as_academic_staff()
        self.client.login(username=self.admin.user.username,
                          password='1234567')
        url = reverse('user:usertoadmin', args=(9999,))
        response = self.client.get(url)
        self.assertContains(response, 'You cannot access this page.')
