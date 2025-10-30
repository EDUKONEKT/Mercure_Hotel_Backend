from django.db import models
from core.models.default_booking import AbstractBooking
from service.models import service


class MealType(models.TextChoices):
    BREAKFAST = "breakfast", "Petit Déjeuner"
    LUNCH = "lunch", "Déjeuner"
    DINNER = "dinner", "Dîner"


class Meal(service):
    meal_type = models.CharField(max_length=20, choices=MealType.choices)

    def save(self, *args, **kwargs):
        self.type = 'restaurant'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_meal_type_display()} - {self.price}€"


class MealBooking(AbstractBooking):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.meal} le {self.date} pour {self.account.user.username}"
