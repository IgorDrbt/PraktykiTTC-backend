from django.urls import path
from .views import ListaKlientow, ListaBiurek

urlpatterns = [
    path('ListaKlientow/', ListaKlientow.as_view(), name='lista_klientow'),
    path('desks/', ListaBiurek.as_view(), name='available_desks'),
]
