from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import Account
from django.contrib.auth.models import User
from spa.models import Spa, SpaBooking


class SaunaBookingTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.account = Account.objects.create(user=self.user, type='Client')
        self.spa = Spa.objects.create(price=50.0, is_available=True, type='spa')

    def test_create_spa_booking(self):
        url = reverse('spabooking-list')  
        data = {
            "spa": self.spa.id,
            "account": self.account.id,
            "check_in": "2025-11-01",
            "check_out": "2025-11-02",
            "total_price": "100.00"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SpaBooking.objects.count(), 1)
        self.assertEqual(SpaBooking.objects.first().spa, self.spa)


    def test_booking_with_invalid_dates(self):
        url = reverse('spabooking-list')
        data = {
           "spa": self.spa.id,
           "account": self.account.id,
           "check_in": "2025-11-03",
           "check_out": "2025-11-01",  
           "total_price": "100.00"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_booking_unavailable_spa(self):
        self.spa.is_available = False
        self.spa.save()

        url = reverse('saunabooking-list')
        data = {
           "spa": self.spa.id,
           "account": self.account.id,
           "check_in": "2025-11-01",
           "check_out": "2025-11-02",
           "total_price": "100.00"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)  

    def test_get_booking(self):
        booking = SpaBooking.objects.create(
           spa=self.spa,
           account=self.account,
           check_in="2025-11-01",
           check_out="2025-11-02",
           total_price="100.00"
        )
        url = reverse('spabooking-detail', args=[booking.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], booking.id)

    def test_total_price_auto_calculated(self):
        url = reverse('spabooking-list')
        data = {
           "spa": self.spa.id,
           "account": self.account.id,
           "check_in": "2025-11-01",
           "check_out": "2025-11-03", 
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        booking = SpaBooking.objects.first()
        expected_total = self.spa.price * 2  
        self.assertEqual(float(booking.total_price), float(expected_total))
    
    
    