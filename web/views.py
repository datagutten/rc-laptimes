import datetime

from django.shortcuts import render

from laptimes import models

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
    return render(request, 'web/infoscreen/infoscreen.html',
                  {
                      'config': config,
                  })


def laps(request):
    decoder = request.GET.get('decoder')
    return render(request, 'web/infoscreen/table.html', {
        'laps': models.Lap.objects.filter(decoder_id=decoder).order_by('-passing1__timestamp')[:50],
        'time': datetime.datetime.now().strftime('%H:%M:%S'),
        'config': config,
    })


def diag(request):
    decoder = request.GET.get('decoder')
    return render(request, 'web/diag.html', {
        'passings': models.Passing.objects.filter(decoder_id=decoder)[:50],
        'config': config,
    })
