from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import Account
from django.contrib.auth.models import User
from fitness.models import Fitness, FitnessBooking


class FitnessBookingTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='fituser', password='testpass')
        self.account = Account.objects.create(user=self.user, type='Client')
        self.fitness = Fitness.objects.create(
            flour=1,
            number=101,
            max_pers=10,
            price=40.0,
            is_available=True,
            type='fitness'
        )

    def test_create_fitness_booking_success(self):
        """✅ Réservation Fitness réussie."""
        url = reverse('fitnessbooking-list')
        data = {
            "fitness": self.fitness.id,
            "account": self.account.id,
            "check_in": "2025-11-01",
            "check_out": "2025-11-03",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        booking = FitnessBooking.objects.first()
        expected_total = self.fitness.price * 2
        self.assertEqual(float(booking.total_price), float(expected_total))

    def test_invalid_dates(self):
        """❌ Refuse la réservation si la date de fin < date de début."""
        url = reverse('fitnessbooking-list')
        data = {
            "fitness": self.fitness.id,
            "account": self.account.id,
            "check_in": "2025-11-05",
            "check_out": "2025-11-03",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_unavailable_fitness(self):
        """❌ Refuse la réservation si la salle n'est pas disponible."""
        self.fitness.is_available = False
        self.fitness.save()

        url = reverse('fitnessbooking-list')
        data = {
            "fitness": self.fitness.id,
            "account": self.account.id,
            "check_in": "2025-11-01",
            "check_out": "2025-11-02",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_get_booking_detail(self):
        """✅ Récupération d’une réservation spécifique."""
        booking = FitnessBooking.objects.create(
            fitness=self.fitness,
            account=self.account,
            check_in="2025-11-01",
            check_out="2025-11-03",
            total_price=80.0
        )
        url = reverse('fitnessbooking-detail', args=[booking.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], booking.id)
