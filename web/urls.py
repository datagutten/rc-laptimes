from django.urls import path

from web import views

app_name = 'laptimes'
urlpatterns = [
    path('', views.index, name='index'),
    path('infoscreen', views.infoscreen, name='infoscreen'),
    path('diag', views.diag, name='diag'),
    path('laps', views.laps, name='laps'),
    path('sessions', views.sessions, name='sessions')
]
