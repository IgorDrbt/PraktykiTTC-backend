# DeskBooking/urls.py
from django.contrib import admin
from django.urls import path, include  # Ensure include is imported

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('Bookingapp.urls')),  # Make sure Bookingapp.urls is included here
]
