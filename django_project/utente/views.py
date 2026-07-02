from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django import forms
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.shortcuts import redirect, render
from .models import CustomUser
#TODO aggiornare il readme e magari mettere padssword più profesionali

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
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('eventi:lista_eventi')


# LoginView per organizzatori
class OrganizerLoginView(LoginView):
    form_class = OrganizerAuthForm
    template_name = 'login_organizer.html'

    def get_success_url(self):
        return reverse_lazy('eventi:lista_eventi')

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('utente:login')


def logout_view(request):
    logout(request)
    messages.info(request, "Hai effettuato il logout.")
    return redirect('utente:login')

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name')


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserUpdateForm
    template_name = 'update_profile.html'
    success_url = reverse_lazy('eventi:lista_eventi')

    # l'utente può modificare solo se stesso
    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Profilo aggiornato con successo!")
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'delete_confirm.html'

    def get_success_url(self):
        messages.warning(self.request, "Il tuo account è stato eliminato definitivamente.")
        return reverse_lazy('utente:login')

    #l'utente può eliminare solo se stesso
    def get_object(self, queryset=None):
        return self.request.user

# Form per promuovere a organizzatore un utente già esistente
class PromoteToOrganizerForm(forms.Form):
    username = forms.CharField(label="Username da promuovere")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            self.user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise ValidationError("Nessun utente trovato con questo username.")
        if self.user.is_organizer:
            raise ValidationError("Questo utente è già un organizzatore.")
        return username

# Form per creare un nuovo organizzatore da zero
class OrganizerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_organizer = True
        if commit:
            user.save()
        return user

class MakeOrganizerView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'make_organizer.html'

    def test_func(self):
        # solo un organizzatore può accedere a questa pagina
        return self.request.user.is_organizer

    def get(self, request, *args, **kwargs):
        context = {
            'promote_form': PromoteToOrganizerForm(),
            'create_form': OrganizerCreationForm(),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        promote_form = PromoteToOrganizerForm()
        create_form = OrganizerCreationForm()

        if 'promote_submit' in request.POST:
            promote_form = PromoteToOrganizerForm(request.POST)
            if promote_form.is_valid():
                user = promote_form.user
                user.is_organizer = True
                user.save()
                messages.success(request, f"L'utente '{user.username}' è ora un organizzatore.")
                return redirect('utente:make_organizer')

        elif 'create_submit' in request.POST:
            create_form = OrganizerCreationForm(request.POST)
            if create_form.is_valid():
                user = create_form.save()
                messages.success(request, f"Nuovo organizzatore '{user.username}' creato con successo.")
                return redirect('utente:make_organizer')

        return render(request, self.template_name, {
            'promote_form': promote_form,
            'create_form': create_form,
        })