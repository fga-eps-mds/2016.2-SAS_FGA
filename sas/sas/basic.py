from django.contrib.auth.models import Group, Permission, User
from user.models import UserProfile
from booking.factories import BookingFactory

class Configuration():


    def get_permission(self, name):
        permissions = Permission.objects.filter(codename=name)
        if permissions.count() > 0:
            return permissions[0]

        return None


    def create_groups(self):
        admin, created = Group.objects.get_or_create(name="admin")
        permission1 = self.get_permission(name = "delete_booking")
        admin.permissions.add(permission1)
        permission2 = self.get_permission(name = "add_booking")
        admin.permissions.add(permission2)
        permission3 = self.get_permission(name = "change_booking")
        admin.permissions.add(permission3)
        permission4 = self.get_permission(name = "delete_userprofile")
        admin.permissions.add(permission4)
        permission5 = self.get_permission(name = "add_userprofile")
        admin.permissions.add(permission5)
        permission6 = self.get_permission(name = "change_userprofile")
        admin.permissions.add(permission6)
        permission7 = self.get_permission(name = "delete_user")
        admin.permissions.add(permission7)
        permission8 = self.get_permission(name = "add_user")
        admin.permissions.add(permission8)
        permission9 = self.get_permission(name = "change_user")
        admin.permissions.add(permission9)
        permission10 = self.get_permission(name = "delete_place")
        admin.permissions.add(permission10)
        permission11 = self.get_permission(name = "add_place")
        admin.permissions.add(permission11)
        permission12 = self.get_permission(name = "change_place")
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

    def create_users(self):
        userprofile = UserProfile()
        userprofile.name("Teste Testando")
        userprofile.registration_number = "110030987"
        userprofile.category = 'Student'
        userprofile.user.username = "test@test.com"
        userprofile.user.email = "test@test.com"
        userprofile.user.set_password('123456')
        userprofile.save()
        userprofile.make_as_academic_staff()
        userprofile.save()
        userprofile = UserProfile()
        userprofile.name("Michel Temer")
        userprofile.registration_number = "110030988"
        userprofile.category = 'Student'
        userprofile.user.username = "michel@planalto.gov.com"
        userprofile.user.email = "michel@planalto.gov.com"
        userprofile.user.set_password('123456')
        userprofile.save()
        userprofile.make_as_academic_staff()
        userprofile.save()
        userprofile = UserProfile()
        userprofile.name("Fernando Henrique Cardoso")
        userprofile.registration_number = "110030989"
        userprofile.category = 'Student'
        userprofile.user.username = "fhc@planalto.gov.com"
        userprofile.user.email = "fhc@planalt.gov.com"
        userprofile.user.set_password('123456')
        userprofile.save()
        userprofile.make_as_admin()
        userprofile.save()
        superuser = User.objects.create_superuser(username="admin",password="123", email="t@t.com")
        superuser.save()

    def create_bookings(self):
        try:
            user = User.objects.get(username="fhc@planalto.gov.com")
        except User.DoesNotExist:
            self.create_groups()
            self.create_users()
            user = User.objects.get(username="fhc@planalto.gov.com")

        b = BookingFactory(name="Teste Fhc",user=user)    
        user = User.objects.get(username="michel@planalto.gov.com")
        b = BookingFactory(name="Teste Michel",user=user)
        user = User.objects.get(username="test@test.com")
        b = BookingFactory(name="Teste Test",user=user)
