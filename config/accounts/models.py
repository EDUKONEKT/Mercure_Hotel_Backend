from django.contrib.auth.models import User
from django.db import models

class AccountType(models.TextChoices):
    CLIENT = "Client"
    ADMIN = "Admin"
    RECEPTIONIST = "Receptionist"

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=AccountType.choices)

    def __str__(self):
        return f"{self.user.username} - {self.type}"
