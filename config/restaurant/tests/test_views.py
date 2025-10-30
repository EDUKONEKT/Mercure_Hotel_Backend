from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import Account
from django.contrib.auth.models import User
from restaurant.models import Meal, MealBooking


class MealBookingTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='mealuser', password='testpass')
        self.account = Account.objects.create(user=self.user, type='Client')
        self.meal = Meal.objects.create(
            meal_type='lunch',
            price=25.0,
            is_available=True,
            type='restaurant'
        )

    def test_create_meal_booking_success(self):
        """✅ Création d'une réservation de repas réussie."""
        url = reverse('mealbooking-list')
        data = {
            "meal": self.meal.id,
            "account": self.account.id,
            "date": "2025-11-01",
            "quantity": 3,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        booking = MealBooking.objects.first()
        expected_total = float(self.meal.price) * 3
        self.assertEqual(float(booking.total_price), float(expected_total))

    def test_past_date_invalid(self):
        """❌ Refuse la réservation si la date est passée."""
        url = reverse('mealbooking-list')
        data = {
            "meal": self.meal.id,
            "account": self.account.id,
            "date": "2020-01-01",
            "quantity": 2,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_unavailable_meal(self):
        """❌ Refuse la réservation si le repas n'est pas disponible."""
        self.meal.is_available = False
        self.meal.save()
        url = reverse('mealbooking-list')
        data = {
            "meal": self.meal.id,
            "account": self.account.id,
            "date": "2025-11-02",
            "quantity": 1,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
