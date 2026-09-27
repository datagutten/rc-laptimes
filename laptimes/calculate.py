import datetime
from zoneinfo import ZoneInfo

from django.conf import settings
from django.db import IntegrityError

from laptimes import models


def lap_time(passing1: models.Passing, passing2: models.Passing, min_limit=10, max_limit=60):
    round_time = passing2.timestamp - passing1.timestamp
    if round_time < min_limit * 1000 or round_time > max_limit * 1000:
        return None
    return round_time


def laptimes(decoder: int = None, transponder_id: int = None):
    passings = models.Passing.objects.filter(lap=None).select_related('decoder').order_by('-timestamp')
    if decoder:
        passings = passings.filter(decoder_id=decoder)
    if transponder_id:
        passings = passings.filter(transponder_id=transponder_id)
    previous_passing: dict[str, models.Passing] = {}
    for passing in passings:
        if passing.time is None:
            passing.time = convert_mylaps_time(passing.timestamp)
            passing.save()

        next_passing = previous_passing.get(passing.transponder_id)
        if next_passing is not None and next_passing.timestamp != passing.timestamp:
            diff = lap_time(passing, next_passing, passing.decoder.min_lap_time, passing.decoder.max_lap_time)
            if diff is not None:
                lap_obj = models.Lap(
                    decoder=passing.decoder,
                    transponder_id=passing.transponder_id,
                    passing1=passing,
                    passing2=next_passing,
                    lap_time_ms=diff,
                    lap_time=datetime.timedelta(milliseconds=diff),
                )

                try:
                    print(lap_obj)
                    lap_obj.save()
                except IntegrityError:
                    pass

        if not next_passing or passing.timestamp != previous_passing[passing.transponder_id].timestamp:
            previous_passing[passing.transponder_id] = passing
    pass


def save_session(laps):
    session_obj = models.Session(transponder_id=laps[0].transponder_id, date=laps[0].passing1.time.date())
    session_obj.save()
    for session_lap in laps:
        session_obj.laps.add(session_lap)
    return session_obj


def create_sessions(decoder: int = None, transponder_id: int = None):
    previous_laps = {}
    session_laps = {}
    laptimes(decoder, transponder_id)
    laps = models.Lap.objects.filter(session=None).order_by('passing1__time')
    if decoder:
        laps = laps.filter(decoder_id=decoder)
    if transponder_id:
        laps = laps.filter(transponder_id=transponder_id)

    for lap in laps:
        transponder = lap.transponder_id
        previous_lap = previous_laps.get(transponder)
        session_laps.setdefault(transponder, []).append(lap)
        if not previous_lap:
            previous_laps[transponder] = lap
            continue
        diff = lap.passing1.time - previous_lap.passing1.time

        if diff.total_seconds() > (lap.decoder.max_lap_time or 60):
            save_session(session_laps[transponder])
            del session_laps[transponder]
        previous_laps[transponder] = lap
    for transponder_id, laps in session_laps.items():
        save_session(laps)


def convert_mylaps_time(timestamp: int):
    """
    MyLaps timestamp seems to be two hours off, local time?
    """
    tz = ZoneInfo(settings.TIME_ZONE)
    time_obj = datetime.datetime.fromtimestamp(timestamp / 1000, tz)
    time_obj_utc = time_obj.astimezone(datetime.timezone.utc).replace(tzinfo=None)
    return time_obj_utc
