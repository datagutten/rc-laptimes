from django.contrib import admin

from laptimes import models


@admin.register(models.Decoder)
class DecoderAdmin(admin.ModelAdmin):
    list_display = ['name', 'ip', 'decoder_type', 'min_lap_time', 'max_lap_time']
    list_filter = ['decoder_type']


@admin.register(models.Lap)
class LapAdmin(admin.ModelAdmin):
    list_display = ['decoder', 'transponder', 'lap_time_ms', 'lap_time', 'start', 'end']
    list_filter = ['decoder', 'transponder', 'lap_time']


@admin.register(models.Passing)
class PassingAdmin(admin.ModelAdmin):
    list_display = ['decoder', 'transponder', 'timestamp', 'saved_time']
    list_filter = ['decoder', 'transponder', 'saved_time']
    readonly_fields = ['raw']


@admin.register(models.Transponder)
class TransponderAdmin(admin.ModelAdmin):
    list_display = ['number', 'name', 'transponder_type']
    list_filter = ['transponder_type']


@admin.register(models.Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['transponder', 'start_time', 'lap_count', 'total_time', 'best_lap', 'avg_lap']
    list_filter = ['laps__decoder', 'transponder']
