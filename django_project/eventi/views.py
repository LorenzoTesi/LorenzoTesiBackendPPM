from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect

from prenotazioni.models import Prenotazione
from .models import Evento


class EventoListView(LoginRequiredMixin, ListView):
    model = Evento
    template_name = 'lista_eventi.html'
    context_object_name = 'eventi'
    def get_queryset(self):
        user = self.request.user
        query = self.request.GET.get('q', '')

        #se chi cerca è un organizzatore allora può cercare solo gli eventi da lui creati
        if user.is_organizer:
            queryset = Evento.objects.filter(organizzatore=user)
            if query:
                queryset = queryset.filter(titolo__icontains=query)
            return queryset
        else:
            if query:
                return Evento.objects.filter(titolo__icontains=query)
            return Evento.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        query = self.request.GET.get('q', '')

        context['query'] = query

        if not user.is_organizer:
            prenotazioni_utente = Prenotazione.objects.filter(utente=user).select_related('evento')
            context['eventi_iscritti'] = [p.evento for p in prenotazioni_utente]
            context['id_eventi_iscritti'] = [p.evento.id for p in prenotazioni_utente]
            if query:
                context['risultati_ricerca'] = Evento.objects.filter(titolo__icontains=query)

        return context


class EventoDetailView(LoginRequiredMixin, DetailView):
    model = Evento
    template_name = 'dettaglio_evento.html'
    context_object_name = 'evento'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        evento = self.object
        user = self.request.user

        posti_occupati = Prenotazione.objects.filter(evento=evento).count()
        context['posti_occupati'] = posti_occupati
        if user.is_organizer:
            prenotazioni = Prenotazione.objects.filter(evento=evento).select_related('utente')
            context['iscritti_username'] = [p.utente.username for p in prenotazioni]
        else:
            context['gia_prenotato'] = Prenotazione.objects.filter(utente=user, evento=evento).exists()
        return context


class OrganizerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_organizer

    def handle_no_permission(self):
        messages.error(self.request, "Azione consentita solo agli organizzatori.")
        return redirect('eventi:lista_eventi')


class EventoCreateView(LoginRequiredMixin, OrganizerRequiredMixin, CreateView):
    model = Evento
    template_name = 'form_evento.html'
    fields = ['titolo', 'descrizione', 'data_ora', 'luogo', 'capienza_massima']
    success_url = reverse_lazy('eventi:lista_eventi')

    def form_valid(self, form):
        form.instance.organizzatore = self.request.user
        messages.success(self.request, "Evento creato con successo!")
        return super().form_valid(form)


class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        evento = self.get_object()
        return self.request.user == evento.organizzatore

    def handle_no_permission(self):
        messages.error(self.request, "Non sei l'organizzatore di questo evento.")
        return redirect('eventi:lista_eventi')

#solo chi ha creato l'evento può modificarlo o cancellarlo
class EventoUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Evento
    template_name = 'form_evento.html'
    fields = ['titolo', 'descrizione', 'data_ora', 'luogo', 'capienza_massima']

    def get_success_url(self):
        messages.success(self.request, "Evento aggiornato con successo!")
        return reverse_lazy('eventi:dettaglio_evento', kwargs={'pk': self.object.pk})


class EventoDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Evento
    template_name = 'cancella_evento.html'
    success_url = reverse_lazy('eventi:lista_eventi')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Evento eliminato definitivamente.")
        return super().delete(request, *args, **kwargs)