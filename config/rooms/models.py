from django.db import models
from core.models.default_booking import AbstractBooking
from service.models import service


class RoomType(models.TextChoices):
    SUITE = "Suite"
    SINGLE = "Single"
    DOUBLE = "Double"
    TRIPLE = "Triple"
    ROMANTIC = "Romantic"
    EROTIC = "Erotic"


class Room(service):
    number = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=20, choices=RoomType.choices)

    def save(self, *args, **kwargs):
        self.type = 'rooms'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.number} - {self.name}"


class RoomBooking(AbstractBooking):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()

    def __str__(self):
        return f"Booking {self.room} du {self.check_in} au {self.check_out}"


    # Create your models here.