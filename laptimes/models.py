from decimal import Decimal

from django.db import models
import datetime


class Decoder(models.Model):
    ip = models.CharField(help_text='Decoder IP or hostname')
    port = models.IntegerField(blank=True, null=True)
    name = models.CharField(blank=True, null=True)
    decoder_type = models.CharField(choices=(('mylaps', 'MyLaps'), ('openstint', 'OpenStint')))
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name or self.ip


class Transponder(models.Model):
    number = models.BigIntegerField()
    name = models.CharField(blank=True, null=True)
    transponder_type = models.TextField()

    def __str__(self):
        return f'{self.transponder_type}: {self.name or self.number}'

    def display(self):
        return self.name or self.number


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

    class Meta:
        ordering = ['-timestamp']


class Session(models.Model):
    transponder = models.ForeignKey(Transponder, on_delete=models.CASCADE, related_name='sessions')
    passings = models.ManyToManyField(Passing)

    def best_lap(self):
        raise NotImplementedError()

    def avg_lap(self):
        raise NotImplementedError()

    def median_lap(self):
        raise NotImplementedError()
