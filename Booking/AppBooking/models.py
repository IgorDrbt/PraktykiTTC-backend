from django.db import IntegrityError, models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.contrib import admin

class Desk(models.Model):
    number = models.AutoField(primary_key=True)  # Auto increment for unique desk numbers
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Desk {self.number} - {'Available' if self.is_available else 'Occupied'}"


class Login(models.Model):
    id_login = models.AutoField(primary_key=True)
    login = models.CharField(max_length=20)
    passwd = models.CharField(max_length=30)

    def clean(self):
        if len(self.passwd) < 8 or not any(c.isdigit() for c in self.passwd):
            raise ValidationError("Hasło musi mieć co najmniej 8 znaków i zawierać cyfrę")

    def save(self, *args, **kwargs):
        if self.passwd:  # Check if password is set
            self.passwd = make_password(self.passwd)  # Hash password before saving
        super().save(*args, **kwargs)


class Worker(models.Model):
    id_worker = models.AutoField(primary_key=True)
    id_login = models.ForeignKey(Login, on_delete=models.SET_NULL, null=True)
    name_worker = models.CharField(max_length=30)
    surname_worker = models.CharField(max_length=30)

    def clean(self):
        if not self.name_worker.isalpha() or not self.surname_worker.isalpha():
            raise ValidationError("Imię i nazwisko mają zawierać litery")


class Reservation(models.Model):
    id_number_table = models.AutoField(primary_key=True)
    reservation_time = models.DateField()
    id_worker = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True)
    desk = models.ForeignKey(Desk, on_delete=models.SET_NULL, null=True)

    def clean(self):
        if self.reservation_time < timezone.now().date():
            raise ValidationError("Nie cofamy się w czasie")
        
        if Reservation.objects.filter(id_worker=self.id_worker, reservation_time=self.reservation_time).exclude(pk=self.pk).exists():
            raise ValidationError("Pracownik jest już zarejestrowany")

        if Reservation.objects.filter(desk=self.desk, reservation_time=self.reservation_time).exclude(pk=self.pk).exists():
            raise ValidationError("To biurko jest już zajęte")
    
    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            raise ValidationError("Nie udało się zapisać rezerwacji, spróbuj ponownie.")
