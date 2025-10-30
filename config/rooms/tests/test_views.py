from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import Account
from django.contrib.auth.models import User
from rooms.models import Room, RoomBooking


class RoomBookingTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.account = Account.objects.create(user=self.user, type='Client')
        self.room = Room.objects.create(number=101, name='Suite', price=100.0, is_available=True, type='rooms')

    def test_create_room_booking(self):
        """✅ Création réussie d’une réservation de chambre."""
        url = reverse('roombooking-list')
        data = {
            "room": self.room.id,
            "account": self.account.id,
            "check_in": "2025-12-01",
            "check_out": "2025-12-03",
            "total_price": "200.00"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RoomBooking.objects.count(), 1)
        self.assertEqual(RoomBooking.objects.first().room, self.room)

    def test_booking_with_invalid_dates(self):
        """❌ Refus si la date de sortie est avant la date d’entrée."""
        url = reverse('roombooking-list')
        data = {
            "room": self.room.id,
            "account": self.account.id,
            "check_in": "2025-12-05",
            "check_out": "2025-12-03",
            "total_price": "200.00"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_booking_unavailable_room(self):
        """❌ Refus si la chambre est marquée comme indisponible."""
        self.room.is_available = False
        self.room.save()

        url = reverse('roombooking-list')
        data = {
            "room": self.room.id,
            "account": self.account.id,
            "check_in": "2025-12-01",
            "check_out": "2025-12-03",
            "total_price": "200.00"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_get_booking(self):
        """✅ Lecture d’une réservation existante."""
        booking = RoomBooking.objects.create(
            room=self.room,
            account=self.account,
            check_in="2025-12-01",
            check_out="2025-12-03",
            total_price="200.00"
        )

        url = reverse('roombooking-detail', args=[booking.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], booking.id)

    def test_total_price_auto_calculated(self):
        """✅ Calcul automatique du prix total selon la durée."""
        url = reverse('roombooking-list')
        data = {
            "room": self.room.id,
            "account": self.account.id,
            "check_in": "2025-12-01",
            "check_out": "2025-12-03",
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        booking = RoomBooking.objects.first()
        expected_total = self.room.price * 2  # 2 jours
        self.assertEqual(float(booking.total_price), float(expected_total))
