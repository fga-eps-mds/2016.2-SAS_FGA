from django.core.management.commands.migrate import Command as BaseCommand
from django.core.management import call_command

class Command(BaseCommand):


    def handle(self,*args,**options):
        output = super(Command,self).handle(*args,**options)
        call_command('loaddata','user/fixtures/group.json')
        call_command('loaddata','booking/fixtures/buildings.json')
        call_command('loaddata','booking/fixtures/places.json')
        return output
