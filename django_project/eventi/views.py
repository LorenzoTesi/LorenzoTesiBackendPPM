from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect
from .models import Evento


class EventoListView(LoginRequiredMixin, ListView):
    model = Evento
    template_name = 'eventi/lista_eventi.html'
    context_object_name = 'eventi'
    ordering = ['data_ora']


class EventoDetailView(LoginRequiredMixin, DetailView):
    model = Evento
    template_name = 'eventi/dettaglio_evento.html'
    context_object_name = 'evento'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gia_prenotato'] = self.object.iscritti.filter(utente=self.request.user).exists()
        return context


class OrganizerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_organizer

    def handle_no_permission(self):
        messages.error(self.request, "Azione consentita solo agli organizzatori.")
        return redirect('eventi:lista_eventi')


class EventoCreateView(LoginRequiredMixin, OrganizerRequiredMixin, CreateView):
    model = Evento
    template_name = 'eventi/form_evento.html'
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
    template_name = 'eventi/form_evento.html'
    fields = ['titolo', 'descrizione', 'data_ora', 'luogo', 'capienza_massima']

    def get_success_url(self):
        messages.success(self.request, "Evento aggiornato con successo!")
        return reverse_lazy('eventi:dettaglio_evento', kwargs={'pk': self.object.pk})


class EventoDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Evento
    template_name = 'eventi/conferma_elimina.html'
    success_url = reverse_lazy('eventi:lista_eventi')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Evento eliminato definitivamente.")
        return super().delete(request, *args, **kwargs)