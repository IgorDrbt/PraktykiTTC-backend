from django.urls import path
from .views import ListaKlientow, UserRegistrationView, DeskReservationView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('ListaKlientow/', ListaKlientow.as_view(), name='lista_klientow'),
    path('login/', TokenObtainPairView.as_view(), name='api_obtain_pair'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('reserve/', DeskReservationView.as_view(), name='reserve_desk'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
