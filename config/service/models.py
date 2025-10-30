from django.db import models


class service(models.Model):
    SERVICE_TYPE = [
        ('rooms','Rooms'),
        ('car_rent','Car_Rent'),
        ('fitness','Fitness'),
        ('restaurant','Restaurant'),
        ('sauna','Sauna'),
        ('spa','Spa'),
        ('meeting_room','Meeting_Room'),

    ]

    
    type = models.CharField(max_length=20, choices=SERVICE_TYPE)
    is_available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=8,decimal_places=2)
    

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.get_type_display()} | {self.price}€ | {'Disponible' if self.is_available else 'Indisponible'}"

    