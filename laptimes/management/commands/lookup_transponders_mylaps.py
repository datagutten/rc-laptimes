import logging
import os
import sys
from logging import Logger

import requests
from django.core.files.base import ContentFile
from django.core.management import BaseCommand

from laptimes import models
from laptimes.speedhive import MyLapsSpeedHive
from rclaptimes import settings

logger: Logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))

mylaps = MyLapsSpeedHive()


class Command(BaseCommand):
    help = 'Clear passings with same timestamp'

    def add_arguments(self, parser):
        parser.add_argument('decoder', nargs='?', type=str)

    def handle(self, *args, **options):
        tracks = os.environ.get('SPEEDHIVE_IDS', '').split(' ')
        media_path = os.path.join(settings.MEDIA_ROOT)
        for track in tracks:
            activities = mylaps.activities(track)
            for activity in activities:

                transponder, created = models.Transponder.objects.get_or_create(
                    number=activity['chipCode'],
                    transponder_type='AMB',
                )

                image_url = f"https://usersandproducts-api.speedhive.com/api/v2/image/id/{activity['gaUId']}"
                if not transponder.avatar:
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        transponder.avatar.save(f'{transponder.number}.png', ContentFile(response.content), save=True)

                if transponder.name != activity['chipLabel']:
                    transponder.name = activity['chipLabel']
                    transponder.save()

                pass
            pass
