from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_organizer = models.BooleanField(
        default=False,
        help_text="Indica se l'utente è un Organizzatore, se deselezionato è un mero partecipante."
    )

    def __str__(self):
        return f"{self.username} ({'Organizzatore' if self.is_organizer else 'Partecipante'})"