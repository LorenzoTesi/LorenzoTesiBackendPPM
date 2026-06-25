from django.db import models

# Create your models here.
from django.conf import settings
from eventi.models import Evento

class Prenotazione(models.Model):
    utente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    data_prenotazione = models.DateTimeField(auto_now_add=True)

    class Meta:
        #per impedire allo stesso utente di prenotarsi due volte allo stesso evento
        unique_together = ('utente', 'evento')