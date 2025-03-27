from django.urls import path
from .views import ListaKlientow
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('ListaKlientow/', ListaKlientow.as_view(), name='lista_klientow'),
    path('login/', obtain_auth_token, name='api_token_auth'),
]
