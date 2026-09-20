from laptimes import models
from . import savers


def get_saver(decoder: models.Decoder):
    savers_cls = {
        'openstint': savers.OpenStintPassingSaver,
        'mylaps': savers.MyLapsPassingSaver,
    }
    return savers_cls.get(decoder.decoder_type)(decoder)
