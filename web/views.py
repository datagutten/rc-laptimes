import datetime

from django.shortcuts import render

from laptimes import models, calculate

config = {
    'round_limit': 20,  # Number of rounds to show
    'only_today': False,  # Only show today's rounds
    'hide_avatars': False,  # Hide driver avatars
    'disable_button': True,  # Show button to disable refresh
    'refresh_interval': 30,  # Refresh interval
    'show_nickname': True,
}


# Create your views here.
def index(request):
    return render(request, 'web/index.html')


def infoscreen(request):
    decoder = request.GET.get('decoder')
    if not decoder:
        return select_decoder(request, 'infoscreen')
    return render(request, 'web/infoscreen/infoscreen.html',
                  {
                      'config': config,
                  })


def infoscreen_table(request):
    decoder = request.GET.get('decoder')
    calculate.laptimes(decoder)
    return render(request, 'web/infoscreen/table.html', {
        'laps': models.Lap.objects.filter(decoder_id=decoder).order_by('-passing1__timestamp')[:50],
        'time': datetime.datetime.now().strftime('%H:%M:%S'),
        'config': config,
    })


def laps(request):
    decoder = request.GET.get('decoder')
    limit = int(request.GET.get('limit', 50))
    calculate.laptimes(decoder)
    laps_obj = models.Lap.objects.select_related('decoder', 'transponder').all().order_by('-passing1__time')
    if decoder:
        laps_obj = laps_obj.filter(decoder_id=decoder)

    return render(request, 'web/laps.html', {'laps': laps_obj[:limit]})


def sessions(request):
    decoder = request.GET.get('decoder')
    if not decoder:
        return select_decoder(request, 'laptimes:sessions')

    transponder = request.GET.get('transponder')
    if transponder:
        transponder_obj = models.Transponder.objects.get(number=transponder)
    else:
        transponder_obj = models.Transponder.objects.exclude(sessions=None).first()

    calculate.create_sessions(int(decoder), transponder_obj.id)
    sessions_obj = models.Session.objects.filter(decoder_id=decoder, transponder=transponder_obj)

    return render(request, 'web/sessions.html', {
        'decoders': models.Decoder.objects.filter(enabled=True),
        'sessions': sessions_obj,
        'transponder': sessions_obj[0].transponder,
        # .order_by('-passing1__timestamp')[:50],
        'time': datetime.datetime.now().strftime('%H:%M:%S'),
    })


def diag(request):
    decoder = request.GET.get('decoder')
    if not decoder:
        return select_decoder(request, 'laptimes:diag')
    return render(request, 'web/diag.html', {
        'decoders': models.Decoder.objects.filter(enabled=True),
        'passings': models.Passing.objects.select_related('transponder').filter(decoder_id=decoder)[:100],
        'config': config,
    })


def select_decoder(request, page: str):
    return render(request, 'web/select_decoder.html', {'decoders': models.Decoder.objects.all(), 'page': page})
