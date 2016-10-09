from django.core.management.base import BaseCommand, CommandError
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
			path = os.path.join(settings.BASE_DIR,app,"migrations")
			if os.path.isdir(path):
				output = call(["rm","-r",path],stderr=STDOUT)
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

	
	
