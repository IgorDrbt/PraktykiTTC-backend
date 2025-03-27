from django.db import models

class Desk(models.Model):
    number = models.IntegerField(unique=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Desk {self.number} - {'Available' if self.is_available else 'Occupied'}"