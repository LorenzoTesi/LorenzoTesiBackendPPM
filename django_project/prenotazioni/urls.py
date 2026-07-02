from django.urls import path

from . import views

app_name = 'prenotazioni'

urlpatterns = [
    path('eventi/<int:evento_id>/prenota/', views.prenota_evento_view, name='prenota_evento'),
    path('eventi/<int:evento_id>/cancella/', views.cancella_prenotazione_view, name='cancella_prenotazione'),
]