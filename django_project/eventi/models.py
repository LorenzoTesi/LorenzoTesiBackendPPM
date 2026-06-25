from django.db import models

# Create your models here.
from django.conf import settings

class Evento(models.Model):
    titolo = models.CharField(max_length=200)
    descrizione = models.TextField()
    data_ora = models.DateTimeField()
    luogo = models.CharField(max_length=200)
    capienza_massima = models.PositiveIntegerField()
    organizzatore = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='eventi_organizzati')

    def __str__(self):
        return self.titolo