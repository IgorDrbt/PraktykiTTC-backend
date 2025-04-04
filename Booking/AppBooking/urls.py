from .views import (
    ListaKlientow,
    LoginView,
    UserRegistrationView,
    DeskReservationView,
    desk_availability_api
)
from .views import ListaKlientow, UserRegistrationView, DeskReservationView
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeskAdminViewSet, WorkerAdminViewSet, ReservationAdminViewSet


router = DefaultRouter()
router.register(r'desks', DeskAdminViewSet)
router.register(r'workers', WorkerAdminViewSet)
router.register(r'reservations', ReservationAdminViewSet)

urlpatterns = [
    path('ListaKlientow/', ListaKlientow.as_view(), name='lista_klientow'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('reserve/', DeskReservationView.as_view(), name='reserve_desk'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('desk-availability/', desk_availability_api, name='desk_availability'),
    path('admin/', include(router.urls)),
]