from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import Account
from django.contrib.auth.models import User
from car_rent.models import Car_rent, CarRentBooking

class CarRentBookingTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.account = Account.objects.create(user=self.user, type='Client')
        self.car = Car_rent.objects.create(
            name="AUDI A3",
            qty=1,
            price=100.0,
            is_available=True,
            type='car_rent'
        )

    def test_create_car_booking(self):
        url = reverse('carrentbooking-list')
        data = {
            "car_rent": self.car.id,
            "account": self.account.id,
            "check_in": "2025-11-01",
            "check_out": "2025-11-03",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        booking = CarRentBooking.objects.first()
        expected_total = self.car.price * 2
        self.assertEqual(float(booking.total_price), float(expected_total))

    def test_invalid_dates(self):
        url = reverse('carrentbooking-list')
        data = {
            "car_rent": self.car.id,
            "account": self.account.id,
            "check_in": "2025-11-05",
            "check_out": "2025-11-03",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_unavailable_car(self):
        self.car.is_available = False
        self.car.save()
        url = reverse('carrentbooking-list')
        data = {
            "car_rent": self.car.id,
            "account": self.account.id,
            "check_in": "2025-11-01",
            "check_out": "2025-11-02",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_double_booking_refused(self):
        CarRentBooking.objects.create(
            car_rent=self.car,
            account=self.account,
            check_in="2025-11-01",
            check_out="2025-11-03",
            total_price=200.00
        )
        url = reverse('carrentbooking-list')
        data = {
            "car_rent": self.car.id,
            "account": self.account.id,
            "check_in": "2025-11-02",
            "check_out": "2025-11-04",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
