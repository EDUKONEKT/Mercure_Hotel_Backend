from django.db import models
from core.models.default_booking import AbstractBooking
from service.models import service
# Create your models here.



class Car_Brand(models.TextChoices):
    FIAT = "FIAT GRANDE PANDA", "Fiat Grande Panda"
    LANCIA = "LANCIA YPSILON 2024", "Lancia Ypsilon 2024"
    LAMBORGHINI = "LAMBORGHINI AVENTADOR", "Lamborghini Aventador"
    AUDI = "AUDI A3", "Audi A3"
    MERCEDES = "MERCEDES CLE", "Mercedes CLE"
    PEUGEOT = "PEUGEOT 3008", "Peugeot 3008"
    RENAULT = "RENAULT CAPTUR", "Renault Captur"
    CITROEN = "CITROEN C5", "Citroën C5"

class Car_rent(service):
    name = models.CharField(max_length=50, choices=Car_Brand.choices)
    qty = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        self.type = 'car_rent'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.qty} disponible(s))"

class CarRentBooking(AbstractBooking):
    car_rent = models.ForeignKey(Car_rent, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()

    def __str__(self):
        return f"Booking {self.car_rent} du {self.check_in} au {self.check_out}"
