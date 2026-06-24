from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_organizer = models.BooleanField(
        default=False,
        help_text="Indica se l'utente può creare e gestire i propri eventi."
    )
    is_attendee = models.BooleanField(
        default=True,
        help_text="Indica se l'utente può iscriversi agli eventi."
    )

    def __str__(self):
        return f"{self.username} ({'Organizzatore' if self.is_organizer else 'Partecipante'})"