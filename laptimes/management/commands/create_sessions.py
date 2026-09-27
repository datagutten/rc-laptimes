from django.core.management import BaseCommand

from laptimes import calculate, models


class Command(BaseCommand):
    help = 'Calculate laptimes from passings'

    def add_arguments(self, parser):
        parser.add_argument('decoder', nargs='?', type=str)

    def handle(self, *args, **options):
        if not options['decoder']:
            for decoder in models.Decoder.objects.filter(enabled=True):
                calculate.create_sessions(decoder.id)
        else:
            calculate.create_sessions(options['decoder'])
