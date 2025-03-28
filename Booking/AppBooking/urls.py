from django.urls import path
from .views import (
    ListaKlientow,
    UserRegistrationView,
    DeskReservationView,
    desk_availability_api
)
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('ListaKlientow/', ListaKlientow.as_view(), name='lista_klientow'),
    path('login/', obtain_auth_token, name='api_token_auth'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('reserve/', DeskReservationView.as_view(), name='reserve_desk'),
    path('desk-availability/', desk_availability_api, name='desk_availability'),
]