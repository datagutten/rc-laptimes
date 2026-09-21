import datetime

from django.db import models
from django.db.models import Avg, Sum, Min


class Decoder(models.Model):
    ip = models.CharField(help_text='Decoder IP or hostname')
    port = models.IntegerField(blank=True, null=True)
    name = models.CharField(blank=True, null=True)
    decoder_type = models.CharField(choices=(('mylaps', 'MyLaps'), ('openstint', 'OpenStint')))
    enabled = models.BooleanField(default=True)
    min_lap_time = models.IntegerField(blank=True, null=True, help_text='Minimum lap time (seconds)')
    max_lap_time = models.IntegerField(blank=True, null=True, help_text='Maximum lap time (seconds)')

    def __str__(self):
        return self.name or self.ip


class Transponder(models.Model):
    number = models.BigIntegerField()
    name = models.CharField(blank=True, null=True)
    transponder_type = models.TextField()
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)

    def __str__(self):
        return f'{self.transponder_type}: {self.name or self.number}'

    def display(self):
        return self.name or self.number

    def days_best(self, day: datetime.date):
        return self.laps.filter(passing1__time__date=day).order_by('lap_time').first()


class Passing(models.Model):
    time = models.DateTimeField(blank=True, null=True)
    timestamp = models.BigIntegerField(help_text='Milliseconds since 1970-01-01')
    decoder = models.ForeignKey(Decoder, on_delete=models.CASCADE, related_name='passings')
    transponder = models.ForeignKey(Transponder, on_delete=models.CASCADE, related_name='passings')
    signal = models.IntegerField()
    hit_count = models.IntegerField()
    voltage = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2)
    temperature = models.IntegerField(blank=True, null=True)
    raw_data = models.BinaryField(blank=True, null=True)

    def __str__(self):
        return f'{self.transponder} {self.timestamp}'

    class Meta:
        ordering = ['-timestamp']


class Lap(models.Model):
    decoder = models.ForeignKey(Decoder, on_delete=models.CASCADE, related_name='laps')
    transponder = models.ForeignKey(Transponder, on_delete=models.CASCADE, related_name='laps')
    passing1 = models.OneToOneField(Passing, on_delete=models.CASCADE, related_name='lap')
    passing2 = models.OneToOneField(Passing, on_delete=models.CASCADE, related_name='lap2')
    lap_time_ms = models.IntegerField()
    lap_time = models.DurationField()

    class Meta:
        get_latest_by = ['passing1__time']

    @property
    def best_time(self) -> Lap:
        return self.transponder.days_best(self.passing1.time.date())

    @property
    def start(self):
        return self.passing1.time

    @property
    def end(self):
        return self.passing2.time

    @property
    def css_class(self):
        if self.best_time.lap_time == self.lap_time:
            return 'best-time'
        else:
            return ''

    def __str__(self):
        return f'{self.transponder} {self.passing1.time} {self.lap_time}'


class Session(models.Model):
    transponder = models.ForeignKey(Transponder, on_delete=models.CASCADE, related_name='sessions')
    date = models.DateField(blank=True, null=True)
    laps = models.ManyToManyField(Lap)

    @property
    def start_time(self):
        return self.laps.first().passing1.time

    @property
    def lap_count(self):
        return self.laps.count()

    def best_lap(self):
        return self.laps.all().aggregate(Min('lap_time'))['lap_time__min']

    def avg_lap(self):
        return self.laps.all().aggregate(Avg('lap_time'))['lap_time__avg']

    def median_lap(self):
        raise NotImplementedError()

    def total_time(self):
        return self.laps.all().aggregate(Sum('lap_time'))['lap_time__sum']
