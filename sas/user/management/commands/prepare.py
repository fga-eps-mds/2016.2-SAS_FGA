from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission, User
from django.conf import settings
from subprocess import call,STDOUT 
from user.models import UserProfile
from sas.basic import Configuration
import os

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
       parser.add_argument("--not-create-groups", 
                            dest="create_groups",
                            action="store_false",
                            default=True,
                            help="It do not create the groups of users") 

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
                self.stdout.write("It will migrate %s %s %s %s" % ("python",self.manage_path(),"makemigrations",app))
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
        self.userprofile = UserProfile()
        self.userprofile.name("Fernando Henrique Cardoso")
        self.userprofile.registration_number = "110030989"
        self.userprofile.category = 'Student'
        self.userprofile.user.username = "fhc@planalto.gov.com"
        self.userprofile.user.email = "fhc@planalt.gov.com"
        self.userprofile.user.set_password('123456')
        self.userprofile.save()
        group = Group.objects.get(name="admin")
        self.userprofile.user.groups.add(group)
        self.userprofile.save()
        superuser = User.objects.create_superuser(username="admin",password="123", email="t@t.com")
        superuser.save()

    def handle(self, *args, **options):
        self.stdout.write("Prepare command")
        if self.is_sqlite():
            if os.path.isfile(self.db_sqlite_path()):
                self.stdout.write("Deleting db")
                call(["rm",self.db_sqlite_path()],stderr=STDOUT)
            self.exclude_migrations()
            output = call(["python",self.manage_path(),"migrate"],stderr=STDOUT)
            if output == 0:
                conf = Configuration()
                if options["create_groups"]:
                    self.stdout.write(self.style.SUCCESS("It will create the groups"))
                    conf.create_groups()

                self.stdout.write(self.style.SUCCESS("It will create the users"))
                self.create_users()	
