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
            diff = lap_time(passing, next_passing)
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
