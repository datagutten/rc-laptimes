from django.core.management import BaseCommand

from laptimes import calculate


class Command(BaseCommand):
    help = 'Calculate laptimes from passings'

    def add_arguments(self, parser):
        parser.add_argument('decoder', nargs='?', type=str)

    def handle(self, *args, **options):
        calculate.create_sessions(options['decoder'])
