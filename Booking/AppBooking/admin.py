from django.contrib import admin
from .models import  Desk, Login, Worker, Reservation
# Register your models here.

admin.site.register(Login)
admin.site.register(Worker)
admin.site.register(Reservation)
admin.site.register(Desk)
