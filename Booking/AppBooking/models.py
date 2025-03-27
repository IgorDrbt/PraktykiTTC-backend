from django.db import models

class Desk(models.Model):
    number = models.IntegerField(unique=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Desk {self.number} - {'Available' if self.is_available else 'Occupied'}"

class Login(models.Model):
    id_login = models.AutoField(primary_key=True)
    login = models.CharField(max_length=20)
    passwd = models.CharField(max_length=30)

class Worker(models.Model):
    id_worker = models.AutoField(primary_key=True)
    id_login = models.ForeignKey(Login, on_delete=models.SET_NULL, null=True)
    name_worker = models.CharField(max_length=30)
    surname_worker = models.CharField(max_length=30)

class Reservation(models.Model):
    id_number_table = models.AutoField(primary_key=True)
    reservation_time = models.DateField()
    id_worker = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True)