from django.db import models

# Model dla biurka
class Desk(models.Model):
    number = models.IntegerField(unique=True)  # Unikalny numer biurka
    is_available = models.BooleanField(default=True)  # Informacja, czy biurko jest dostępne

    def __str__(self):
        return f"Desk {self.number} - {'Available' if self.is_available else 'Occupied'}"

# Model dla logowania użytkowników 
class Login(models.Model):
    id_login = models.AutoField(primary_key=True)
    login = models.CharField(max_length=20)
    passwd = models.CharField(max_length=30)  
    def __str__(self):
        return f"Login {self.login}"

# Model dla pracowników 
class Worker(models.Model):
    id_worker = models.AutoField(primary_key=True)
    id_login = models.ForeignKey(Login, on_delete=models.SET_NULL, null=True)
    name_worker = models.CharField(max_length=30)
    surname_worker = models.CharField(max_length=30)
    position = models.CharField(max_length=30, null=True, blank=True)  # Możemy dodać stanowisko

    def __str__(self):
        return f"{self.name_worker} {self.surname_worker}"

