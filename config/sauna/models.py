from django.db import models
from core.models.default_booking import AbstractBooking
from service.models import service


class Sauna(service):
    name = models.CharField(max_length=100, default="Sauna")

    def save(self, *args, **kwargs):
        self.type = 'sauna'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Sauna - {self.price}€ - {'Disponible' if self.is_available else 'Indisponible'}"
    
class SaunaBooking(AbstractBooking):
    sauna = models.ForeignKey(Sauna, on_delete=models.CASCADE)
    check_in = models.DateField()  
    check_out = models.DateField()  

    def __str__(self):
        return f"Booking {self.sauna} du {self.check_in} au {self.check_out}"
