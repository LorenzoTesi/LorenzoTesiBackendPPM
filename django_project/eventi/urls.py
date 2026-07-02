from django.urls import path

from . import views

app_name = 'eventi'

urlpatterns = [
    path('eventi/', views.EventoListView.as_view(), name='lista_eventi'),
    path('eventi/nuovo/', views.EventoCreateView.as_view(), name='crea_evento'),
    path('eventi/<int:pk>/', views.EventoDetailView.as_view(), name='dettaglio_evento'),
    path('eventi/<int:pk>/modifica/', views.EventoUpdateView.as_view(), name='modifica_evento'),
    path('eventi/<int:pk>/elimina/', views.EventoDeleteView.as_view(), name='elimina_evento'),
]