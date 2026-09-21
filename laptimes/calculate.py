import datetime

from django.db import IntegrityError

from laptimes import models


def lap_time(passing1: models.Passing, passing2: models.Passing, min_limit=10, max_limit=60):
    round_time = passing2.timestamp - passing1.timestamp
    if round_time < min_limit * 1000 or round_time > max_limit * 1000:
        return None
    return round_time


def laptimes(decoder: int = None):
    passings = models.Passing.objects.all().order_by('-timestamp').filter(lap=None)
    if decoder:
        passings = passings.filter(decoder_id=decoder)
    previous_passing: dict[str, models.Passing] = {}
    for passing in passings:
        next_passing = previous_passing.get(passing.transponder)
        if next_passing is not None and next_passing.timestamp != passing.timestamp:
            diff = lap_time(passing, next_passing, passing.decoder.min_lap_time, passing.decoder.max_lap_time)
            if diff is None:
                continue

            lap_obj = models.Lap(
                decoder=passing.decoder,
                transponder=passing.transponder,
                passing1=passing,
                passing2=next_passing,
                lap_time_ms=diff,
                lap_time=datetime.timedelta(milliseconds=diff),
            )

            try:
                print(lap_obj)
                lap_obj.save()
            except IntegrityError:
                continue
            pass

        if not next_passing or passing.timestamp != previous_passing[passing.transponder].timestamp:
            previous_passing[passing.transponder] = passing
    pass


def save_session(laps):
    session_obj = models.Session(transponder_id=laps[0].transponder_id, date=laps[0].passing1.time.date())
    session_obj.save()
    for session_lap in laps:
        session_obj.laps.add(session_lap)
    return session_obj


def create_sessions(decoder: int = None):
    previous_laps = {}
    session_laps = {}
    for lap in models.Lap.objects.filter(session=None).order_by('passing1__time'):
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
