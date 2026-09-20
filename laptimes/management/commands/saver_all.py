from django.core.management import BaseCommand

from laptimes import models
from savers import common
import asyncio


async def saver(decoder: models.Decoder):
    saver_obj = common.PassingSaver.get_saver(decoder)
    saver_obj.run()


async def main():
    for decoder_obj in models.Decoder.objects.filter(enabled=True):
        asyncio.create_task(saver(decoder_obj))


class Command(BaseCommand):
    help = 'Save passings from all decoders'

    def handle(self, *args, **options):
        asyncio.run(main())
