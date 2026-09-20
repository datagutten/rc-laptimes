from django.contrib import admin

from laptimes import models


@admin.register(models.Decoder)
class DecoderAdmin(admin.ModelAdmin):
    list_display = ['name', 'ip', 'decoder_type']


@admin.register(models.Passing)
class PassingAdmin(admin.ModelAdmin):
    list_display = ['decoder', 'transponder', 'timestamp', 'datetime']
    list_filter = ['decoder', 'transponder']
    readonly_fields = ['datetime']


@admin.register(models.Transponder)
class TransponderAdmin(admin.ModelAdmin):
    list_display = ['number', 'name', 'transponder_type']
    list_filter = ['transponder_type']
