from django.core.management.commands.migrate import Command as BaseCommand
from django.core.management import call_command

class Command(BaseCommand):


    def handle(self,*args,**options):
        output = super(Command,self).handle(*args,**options)
        call_command('loaddata','user/fixtures/permissions.json')
        call_command('loaddata','user/fixtures/group.json')
        call_command('loaddata','user/fixtures/users.json')
        call_command('loaddata','user/fixtures/userProfiles.json')
        call_command('loaddata','booking/fixtures/buildings.json')
        call_command('loaddata','booking/fixtures/places.json')
        call_command('loaddata','booking/fixtures/bookTimes.json')
        call_command('loaddata','booking/fixtures/bookings.json')
        
        return output
