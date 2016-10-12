from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission, User
from django.conf import settings
from subprocess import call,STDOUT 
import os
from user.models import UserProfile

class Command(BaseCommand):
	help = 'Closes the specified poll for voting'

	def db_sqlite_path(self):
		return settings.DATABASES['default']['NAME']

	def manage_path(self):	
		return os.path.join(settings.BASE_DIR,"manage.py")

	def is_sqlite(self):
		return "sqlite" in settings.DATABASES['default']['ENGINE']

	def exclude_migrations(self):
		for app in settings.INSTALLED_APPS:
			path_migrations = os.path.join(settings.BASE_DIR,app,"migrations")
			path_app = os.path.join(settings.BASE_DIR,app)
			if os.path.isdir(path_migrations):
				output = call(["rm","-r",path_migrations],stderr=STDOUT)

			if os.path.isdir(path_app):
				print("It will migrate %s %s %s %s" % ("python",self.manage_path(),"makemigrations",app))
				call(["python",self.manage_path(),
					  "makemigrations",app],stderr=STDOUT)

	def create_users(self):
		self.userprofile = UserProfile()
		self.userprofile.name("Teste Testando")
		self.userprofile.registration_number = "110030987"
		self.userprofile.category = 'Student'
		self.userprofile.user.username = "test@test.com"
		self.userprofile.user.email = "test@test.com"
		self.userprofile.user.set_password('123456')
		self.userprofile.save()
		self.userprofile = UserProfile()
		self.userprofile.name("Michel Temer")
		self.userprofile.registration_number = "110030988"
		self.userprofile.category = 'Student'
		self.userprofile.user.username = "michel@planalto.gov.com"
		self.userprofile.user.email = "michel@planalt.gov.com"
		self.userprofile.user.set_password('123456')
		self.userprofile.save()

	def get_permission(self, name):
		permissions = Permission.objects.filter(codename=name)
		if permissions.count() > 0:
			return permissions[0]
		
		return None
		

	def create_groups(self):
		superuser = User.objects.create_superuser(username="admin",password="123", email="t@t.com")
		superuser.save()
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


	def handle(self, *args, **options):
		self.stdout.write("Testing command")
		if self.is_sqlite():
			if os.path.isfile(self.db_sqlite_path()):
				self.stdout.write("Deleting db")
				call(["rm",self.db_sqlite_path()],stderr=STDOUT)
			self.exclude_migrations()
			output = call(["python",self.manage_path(),"migrate"],stderr=STDOUT)
			if output == 0:
				self.create_users()	
				self.create_groups()

	
	
