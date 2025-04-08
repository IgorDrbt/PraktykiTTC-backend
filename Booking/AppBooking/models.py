from django.db import IntegrityError, models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

class Desk(models.Model):
    number = models.AutoField(primary_key=True)  
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
        if self.passwd:  
            self.passwd = make_password(self.passwd)
        super().save(*args, **kwargs)


class Worker(models.Model):
    id_worker = models.AutoField(primary_key=True)
    id_login = models.ForeignKey(Login, on_delete=models.SET_NULL, null=True)
    name_worker = models.CharField(max_length=30)
    surname_worker = models.CharField(max_length=30)

    def clean(self):
        if not self.name_worker.isalpha() or not self.surname_worker.isalpha():
            raise ValidationError("Imię i nazwisko mają zawierać litery")


from django.contrib.auth.models import User  # Import the User model
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.utils import IntegrityError

class Reservation(models.Model):
    id_number_table = models.AutoField(primary_key=True)
    reservation_time = models.DateField()
    id_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Changed to use User model
    desk = models.ForeignKey(Desk, on_delete=models.SET_NULL, null=True)

    def clean(self):
        if self.reservation_time < timezone.now().date():
            raise ValidationError("Nie cofamy się w czasie")
        
        if Reservation.objects.filter(id_user=self.id_user, reservation_time=self.reservation_time).exclude(pk=self.pk).exists():
            raise ValidationError("Użytkownik jest już zarejestrowany")

        if Reservation.objects.filter(desk=self.desk, reservation_time=self.reservation_time).exclude(pk=self.pk).exists():
            raise ValidationError("To biurko jest już zajęte")
    
    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            raise ValidationError("Nie udało się zapisać rezerwacji, spróbuj ponownie.")

