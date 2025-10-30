from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import Account
from django.contrib.auth.models import User
from meeting_room.models import MeetingRoom, MeetingRoomBooking


class MeetingRoomBookingTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='meetinguser', password='testpass')
        self.account = Account.objects.create(user=self.user, type='Client')
        self.room = MeetingRoom.objects.create(
            flour=2,
            number=204,
            max_pers=12,
            price=50.0,
            is_available=True,
            type='meeting_room'
        )

    def test_create_meeting_booking_success(self):
        """✅ Réservation Meeting Room réussie."""
        url = reverse('meetingroombooking-list')
        data = {
            "meeting_room": self.room.id,
            "account": self.account.id,
            "date": "2025-11-05",
            "start_time": "09:00:00",
            "end_time": "12:00:00",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        booking = MeetingRoomBooking.objects.first()
        expected_total = self.room.price * 3  
        self.assertEqual(float(booking.total_price), float(expected_total))

    def test_invalid_time_range(self):
        """❌ Refuse la réservation si heure de fin < heure de début."""
        url = reverse('meetingroombooking-list')
        data = {
            "meeting_room": self.room.id,
            "account": self.account.id,
            "date": "2025-11-05",
            "start_time": "15:00:00",
            "end_time": "13:00:00",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_unavailable_meeting_room(self):
        """❌ Refuse la réservation si la salle n'est pas disponible."""
        self.room.is_available = False
        self.room.save()

        url = reverse('meetingroombooking-list')
        data = {
            "meeting_room": self.room.id,
            "account": self.account.id,
            "date": "2025-11-06",
            "start_time": "09:00:00",
            "end_time": "11:00:00",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_get_meeting_booking_detail(self):
        """✅ Récupération d'une réservation spécifique."""
        booking = MeetingRoomBooking.objects.create(
            meeting_room=self.room,
            account=self.account,
            date="2025-11-07",
            start_time="09:00:00",
            end_time="11:00:00",
            total_price=100.0
        )
        url = reverse('meetingroombooking-detail', args=[booking.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], booking.id)
