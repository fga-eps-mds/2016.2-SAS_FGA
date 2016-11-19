from django.contrib.auth.models import Group, Permission, User
from user.models import UserProfile
from booking.factories import BookingFactory
from user.factories import UserProfileFactory, UserFactory


class Configuration():

    def get_permission(self, name):
        permissions = Permission.objects.filter(codename=name)
        if permissions.count() > 0:
            return permissions[0]

        return None

    def create_groups(self):
        admin, created = Group.objects.get_or_create(name="admin")
        permission1 = self.get_permission(name="delete_booking")
        admin.permissions.add(permission1)
        permission2 = self.get_permission(name="add_booking")
        admin.permissions.add(permission2)
        permission3 = self.get_permission(name="change_booking")
        admin.permissions.add(permission3)
        permission4 = self.get_permission(name="delete_userprofile")
        admin.permissions.add(permission4)
        permission5 = self.get_permission(name="add_userprofile")
        admin.permissions.add(permission5)
        permission6 = self.get_permission(name="change_userprofile")
        admin.permissions.add(permission6)
        permission7 = self.get_permission(name="delete_user")
        admin.permissions.add(permission7)
        permission8 = self.get_permission(name="add_user")
        admin.permissions.add(permission8)
        permission9 = self.get_permission(name="change_user")
        admin.permissions.add(permission9)
        permission10 = self.get_permission(name="delete_place")
        admin.permissions.add(permission10)
        permission11 = self.get_permission(name="add_place")
        admin.permissions.add(permission11)
        permission12 = self.get_permission(name="change_place")
        admin.permissions.add(permission12)
        admin.save()
        academic_staff, created = Group.objects.get_or_create(name="academic_staff")
        academic_staff.permissions.add(permission2)
        academic_staff.permissions.add(permission3)
        academic_staff.permissions.add(permission4)
        academic_staff.permissions.add(permission5)
        academic_staff.permissions.add(permission6)
        academic_staff.permissions.add(permission7)
        academic_staff.permissions.add(permission8)
        academic_staff.permissions.add(permission9)
        academic_staff.save()

    def check_registration_number(self, number):
        try:
            u = UserProfile.objects.filter(registration_number=number)
            return False
        except User.DoesNotExist:
            return True

    def create_users_factories(self, username, name):
        try:
            user = UserFactory(usename=username,
                               name=name,
                               email=username)
            userprofile = UserProfileFactory(user=user)
        except:
            user = User.objects.get(username=username)

        return user

    def create_michel_temer(self):
        userprofile = UserProfile()
        userprofile.name("Michel Temer")
        userprofile.registration_number = "110030988"
        userprofile.category = 'Student'
        userprofile.user.username = "michel@planalto.gov.com"
        userprofile.user.email = "michel@planalto.gov.com"
        userprofile.user.set_password('123456')
        if(not self.check_registration_number(userprofile.registration_number)):
            userprofile.registration_number = "101030988"
        userprofile.save()
        userprofile.make_as_academic_staff()
        userprofile.save()

    def check_user_exists(self, username):
        try:
            user = User.objects.get(username=username)
            return True
        except User.DoesNotExist:
            return False

    def create_test_testando(self):
        userprofile = UserProfile()
        userprofile.name("Teste Testando")
        userprofile.registration_number = "110030987"
        userprofile.category = 'Student'
        userprofile.user.username = "test@test.com"
        userprofile.user.email = "test@test.com"
        userprofile.user.set_password('123456')
        if(not self.check_registration_number(userprofile.registration_number)):
            userprofile.registration_number = "101030987"
        userprofile.save()
        userprofile.make_as_academic_staff()
        userprofile.save()

    def create_fhc(self):
        userprofile = UserProfile()
        userprofile.name("Fernando Henrique Cardoso")
        userprofile.registration_number = "110030989"
        userprofile.category = 'Student'
        userprofile.user.username = "fhc@planalto.gov.com"
        userprofile.user.email = "fhc@planalt.gov.com"
        userprofile.user.set_password('123456')
        if(not self.check_registration_number(userprofile.registration_number)):
            userprofile.registration_number = "101030989"
        userprofile.save()
        userprofile.make_as_admin()
        userprofile.save()

    def create_users(self):
        self.create_test_testanto()
        self.create_michel_temer()
        self.create_fhc()
        superuser = User.objects.create_superuser(username="admin", password="123", email="t@t.com")
        superuser.save()

    def create_bookings(self):
        if(not self.check_user_exists("fhc@planalto.gov.com")):
            self.create_fhc()
            user = User.objects.get(username="fhc@planalto.gov.com")
        b = BookingFactory(name="Teste Fhc", user=user)
        if(not self.check_user_exists("michel@planalto.gov.com")):
            self.create_michel_temer()
            user = User.objects.get(username="michel@planalto.gov.com")
        b = BookingFactory(name="Teste Michel", user=user)
        if(not self.check_user_exists("test@test.com")):
            self.create_test_testando()
            user = User.objects.get(username="test@test.com")
        b = BookingFactory(name="Teste Test", user=user)
