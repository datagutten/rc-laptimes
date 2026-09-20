import logging
import sys

from django.core.management import BaseCommand

from laptimes import models
from laptimes.saver.get_saver import get_saver
from logging import Logger

logger: Logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


class Command(BaseCommand):
    help = 'Save passings from a decoder'

    def add_arguments(self, parser):
        parser.add_argument('decoder', nargs='?', type=str)

    def handle(self, *args, **options):
        decoder_obj = models.Decoder.objects.get(id=options['decoder'])
        saver_obj = get_saver(decoder_obj)
        saver_obj.run()
