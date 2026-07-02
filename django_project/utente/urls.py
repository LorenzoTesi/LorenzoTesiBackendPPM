from django.shortcuts import render

# Create your views here.
from django.urls import path

from . import views

app_name = 'utente'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.ParticipantLoginView.as_view(),
         name='login'),
    path('organizzatore/login/', views.OrganizerLoginView.as_view(),
         name='login_organizer'),
    path('logout/', views.logout_view, name='logout'),
    path('profilo/modifica/', views.UserUpdateView.as_view(), name='update_profile'),
    path('profilo/elimina/', views.UserDeleteView.as_view(), name='delete_account'),
]

#TODO se sei organizzatore loggi dalla pagina dei partecipanti ma entri come organizzatore da fixare
#TODO info, iscriviti e disiscriviti danno pagina di erore ma funzionano correttamente sul db
#TODO manca il tasto per modificare il profilo e cancellarlo
#TODO non funziona pagina per accedere come organizzatori e per registrarsi
#TODO gestione della modifica della capienza di un evento