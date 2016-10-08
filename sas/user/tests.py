from django.test import TestCase, RequestFactory
from user.models import *
from django.test import Client
from django.contrib.auth.models import AnonymousUser
from user.views import delete_user, edit_user
from user.factories import UserFactory, UserProfileFactory
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout

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
        response = self.client.get(url, follow = True)
        self.assertTemplateUsed(response, 'sas/index.html')

    def test_edit_post_registration_number(self):
        request = self.factory.get('/user/edituser/')
        client = self.client
        userprofile = self.userprofile
        client.login(username='gutorc@hotmail.com', password='123456')
        parameters = {'name': 'Pedro','registration_number': '140000000', \
            'category' : '1', 'email' : "gutorc@hotmail.com"}
        response = client.post('/user/edituser/', parameters)
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

    def test_save(self):
        self.userprofile = UserProfile()
        self.userprofile.name("Gustavo Rodrigues Coelho")
        self.userprofile.registration_number = "11/0030559"
        self.userprofile.user.username = "gutorc@hotmail.com"
        self.userprofile.user.email = "gutorc@hotmail.com"
        self.userprofile.save()
        self.assertEqual(self.userprofile.pk, 1)

class LoginTest(TestCase):
    def setUp(self):
        self.user = UserProfileFactory.create()
        self.user.user.set_password('1234567')
        self.user.save()
        self.client = Client()

    def test_get_request(self):
        response = self.client.get('/user/login/', follow = True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain, [('/', 302)])

    def test_invalid_email(self):
        response = self.client.post('/user/login/', {'email' : 'aeiou', 'password' : '1234567'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter a valid email address.')

    def test_invalid_password(self):
        response = self.client.post('/user/login/', {'email' : self.user.user.email, 'password' : '1235567'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Email or Password does not match')

    def test_valid_user(self):
        logout(self.client)
        response = self.client.post('/user/login/', {'email' : self.user.user.email, 'password' : '1234567'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hi, %s' % (self.user.full_name()))

class LogoutTest(TestCase):
    def setUp(self):
        self.user = UserProfileFactory.create()
        self.user.user.set_password('1234567')
        self.user.save()
        self.client = Client()

    def test_logout(self):
        self.client.login(username= self.user.user.email, password= '1234567')
        response = self.client.get('/user/logout/', follow = True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain, [('/', 302)])
        self.assertContains(response, 'You have been logged out successfully!')

    def test_invalid_logout(self):
        response = self.client.get('/user/logout/', follow = True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain, [('/', 302)])
        self.assertNotContains(response, 'You have been logged out sucessfully!')
