from django.db import models
from core.models.default_booking import AbstractBooking
from service.models import service
# Create your models here.


class MeetingRoom(service):
    flour = models.PositiveSmallIntegerField()
    number = models.PositiveIntegerField()
    max_pers = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        self.type = 'meeting_room'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Salle {self.number} (Étage {self.flour}) - Capacité: {self.max_pers} pers"

class MeetingRoomBooking(AbstractBooking):
    meeting_room = models.ForeignKey(MeetingRoom, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.meeting_room} le {self.date} de {self.start_time} à {self.end_time}"
