from django.shortcuts import render

# Create your views here.
from django.urls import path

from . import views

app_name = 'utente'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.ParticipantLoginView.as_view(),
         name='login_attendee'),
    path('organizzatore/login/', views.OrganizerLoginView.as_view(),
         name='login_organizer'),
    path('logout/', views.logout_view, name='logout'),
]