from django.db import models
from core.models.default_booking import AbstractBooking
from service.models import service
# Create your models here.

class Fitness(service):
    flour = models.PositiveSmallIntegerField()
    number = models.PositiveIntegerField()
    max_pers = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        self.type = 'fitness'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Salle {self.number} (Étage {self.flour}) - Capacité: {self.max_pers} personnes"

class FitnessBooking(AbstractBooking):
    fitness = models.ForeignKey(Fitness, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()

    def __str__(self):
        return f"Booking {self.fitness} du {self.check_in} au {self.check_out}"   
        