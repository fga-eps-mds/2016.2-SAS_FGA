from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission, User
from django.conf import settings
from subprocess import call, STDOUT
from user.models import UserProfile
from sas.basic import Configuration
import os
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument("--create-groups",
                            dest="create_groups",
                            action="store_true",
                            default=False,
                            help="it create the groups of users")

        parser.add_argument("--create-users",
                            dest="create_users",
                            action="store_true",
                            default=False,
                            help="It create basic users")

    def db_sqlite_path(self):
        return settings.DATABASES['default']['NAME']

    def manage_path(self):
        return os.path.join(settings.BASE_DIR, "manage.py")

    def is_sqlite(self):
        return "sqlite" in settings.DATABASES['default']['ENGINE']

    def exclude_sqlite(self):
        if os.path.isfile(self.db_sqlite_path()):
            self.stdout.write("Deleting db")
            call(["rm", self.db_sqlite_path()], stderr=STDOUT)

    def exclude_migrations(self):
        for app in settings.INSTALLED_APPS:
            path_migrations = os.path.join(settings.BASE_DIR,
                                           app, "migrations")
            path_app = os.path.join(settings.BASE_DIR, app)
            if os.path.isdir(path_migrations):
                output = call(["rm", "-r", path_migrations], stderr=STDOUT)

            if os.path.isdir(path_app):
                msg = "It will create migrations %s %s %s %s".format(
                      "python",
                      self.manage_path(),
                      "makemigrations",
                      app)
                self.stdout.write(msg)
                call_command('makemigrations', app)

    def handle(self, *args, **options):
        self.stdout.write("Prepare command")
        if self.is_sqlite():
            self.exclude_sqlite()

        self.exclude_migrations()
        if options["create_groups"] and options["create_users"]:
            call_command('migrate', '--not-create-user-fixture')
        else:
            call_command('migrate')
        conf = Configuration()
        if options["create_groups"]:
            self.stdout.write(self.style.SUCCESS("It will create the groups"))
            conf.create_groups()

        if options["create_users"]:
            self.stdout.write(self.style.SUCCESS("It will create the users"))
            self.create_users()
