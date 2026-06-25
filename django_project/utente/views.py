from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'is_organizer',)

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registrazione avvenuta con successo!")
            return redirect('eventi:lista_eventi')
        else:
            messages.error(request, "Errore nella registrazione. Riprova.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'utente/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bentornato, {username}!")
                return redirect('eventi:lista_eventi')
        messages.error(request, "Username o password non validi.")
    else:
        form = AuthenticationForm()
    return render(request, 'utente/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Hai effettuato il logout.")
    return redirect('utente:login')