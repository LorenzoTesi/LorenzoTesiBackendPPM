from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from eventi.models import Evento
from .models import Prenotazione


@login_required
def prenota_evento_view(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)

    if request.user.is_organizer:
        messages.error(request, "Gli organizzatori non possono prenotarsi agli eventi")
        return redirect('eventi:dettaglio_evento', pk=evento.id)

    #controllo se l'utente è già iscritto
    gia_iscritto = Prenotazione.objects.filter(utente=request.user, evento=evento).exists()
    if gia_iscritto:
        messages.warning(request, "Ti sei già iscritto a questo evento")
        return redirect('eventi:dettaglio_evento', pk=evento.id)

    #controllo se ha già raggiunto la capienza massima
    iscritti = Prenotazione.objects.filter(evento=evento).count()
    if iscritti >= evento.capienza_massima:
        messages.error(request, "Spiacente, i posti per questo evento sono esauriti")
        return redirect('eventi:dettaglio_evento', pk=evento.id)

    Prenotazione.objects.create(utente=request.user, evento=evento)
    messages.success(request, f"Prenotazione completata per l'evento: {evento.titolo}!")
    return redirect('eventi:dettaglio_evento', pk=evento.id)


@login_required
def cancella_prenotazione_view(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    prenotazione = Prenotazione.objects.filter(utente=request.user, evento=evento).first()

    if prenotazione:
        prenotazione.delete()
        messages.success(request, "La tua prenotazione è stata cancellata con successo.")
    else:
        messages.error(request, "Nessuna prenotazione trovata per questo evento.")

    return redirect('eventi:dettaglio_evento', pk=evento.id)