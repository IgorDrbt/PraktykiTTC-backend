from django.contrib import admin
from .models import Desk, Login, Worker, Reservation

try:
    admin.site.unregister(Login)
except admin.sites.NotRegistered:
    pass

admin.site.register(Login)

@admin.register(Desk)
class DeskAdmin(admin.ModelAdmin):
    list_display = ('number', 'is_available')
    actions = ['mark_as_unavailable']

    def mark_as_unavailable(self, request, queryset):
        queryset.update(is_available=False)
        self.message_user(request, "Selected desks have been marked as unavailable.")
    mark_as_unavailable.short_description = "Mark selected desks as unavailable"


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('name_worker', 'surname_worker', 'id_login')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('reservation_time', 'id_worker', 'desk')
