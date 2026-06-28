from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.shortcuts import redirect
from .models import CustomUser

#TODO implementare eliminazione dell'account e update dei campi dell'utente, logica per rendere un prfilo un organizatore oppure registrne uno ex novo

# Form registrazione
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email',)

    # is_organizer viene forzato a False nel save
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_organizer = False
        if commit:
            user.save()
        return user


# AuthenticationForm per partecipanti
class ParticipantAuthForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)



# AuthenticationForm per organizzatori
class OrganizerAuthForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.is_organizer:
            raise ValidationError(
                "Non sei un organizzatore, usa il login partecipanti."
            )


# LoginView per partecipanti
class ParticipantLoginView(LoginView):
    form_class = ParticipantAuthForm
    template_name = 'utente/login_attendee.html'

    def get_success_url(self):
        return reverse_lazy('eventi:lista_eventi')


# LoginView per organizzatori
class OrganizerLoginView(LoginView):
    form_class = OrganizerAuthForm
    template_name = 'utente/login_organizer.html'

    def get_success_url(self):
        return reverse_lazy('eventi:lista_organizzatore')


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'utente/register.html'
    success_url = reverse_lazy('utente:login_attendee')


def logout_view(request):
    logout(request)
    messages.info(request, "Hai effettuato il logout.")
    return redirect('utente:login_partecipante')



