from django.db import models
from core.models.default_booking import AbstractBooking
from service.models import service
# Create your models here.


class Spa(service):
    name = models.CharField(max_length=100, default="Spa")
    def save(self, *args, **kwargs):
        self.type = 'spa'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Spa - {self.price}€ - {'Disponible' if self.is_available else 'Indisponible'}"

class SpaBooking(AbstractBooking):
    spa = models.ForeignKey(Spa, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()

    def __str__(self):
        return f"Booking {self.spa} du {self.check_in} au {self.check_out}"
