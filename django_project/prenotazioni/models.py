from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from eventi.models import Evento

class Prenotazione(models.Model):
    # RELAZIONE 2: Legame tra la prenotazione, l'utente e l'evento
    utente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='prenotazioni')
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='iscritti')
    data_prenotazione = models.DateTimeField(auto_now_add=True)

    class Meta:
        #impedisce allo stesso utente di prenotarsi due volte allo stesso evento
        unique_together = ('utente', 'evento')