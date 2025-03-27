from django.urls import path
from .views import ListaKlientow

urlpatterns = [
    path('ListaKlientow/', ListaKlientow.as_view(), name='lista_klientow'),
]
