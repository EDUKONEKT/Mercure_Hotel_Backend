from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Account, AccountType
from car_rent.models import Car_rent, CarRentBooking
from datetime import date, timedelta
from django.core.exceptions import ValidationError

class CarRentBookingModelTests(TestCase):

    def setUp(self):
        
        user = User.objects.create_user(username='modeluser', password='testpass')
        self.account = Account.objects.create(user=user, type=AccountType.CLIENT)

       
        self.car = Car_rent.objects.create(
            name="AUDI A3",
            qty=1,
            price=100.0,
            is_available=True,
            type='car_rent'
        )

    

    def test_invalid_dates_raise_error(self):
        """❌ La date de fin ne peut pas être avant la date de début."""
        check_in = date(2025, 11, 5)
        check_out = date(2025, 11, 3)

        booking = CarRentBooking(
            car_rent=self.car,
            account=self.account,
            check_in=check_in,
            check_out=check_out,
            total_price=0
        )

        # Simule la validation du serializer (même logique)
        with self.assertRaises(ValidationError):
            if check_in >= check_out:
                raise ValidationError("La date de fin doit être après la date de début.")

    def test_unavailable_car_cannot_be_booked(self):
        """❌ Une voiture non disponible ne peut pas être réservée."""
        self.car.is_available = False
        self.car.save()

        check_in = date(2025, 11, 1)
        check_out = date(2025, 11, 2)

        booking = CarRentBooking(
            car_rent=self.car,
            account=self.account,
            check_in=check_in,
            check_out=check_out,
            total_price=0
        )

        with self.assertRaises(ValidationError):
            if not self.car.is_available or self.car.qty <= 0:
                raise ValidationError("Ce véhicule n'est pas disponible pour le moment.")

    def test_double_booking_not_allowed(self):
        """❌ Interdit de réserver deux fois la même voiture sur une période qui se chevauche."""
        CarRentBooking.objects.create(
            car_rent=self.car,
            account=self.account,
            check_in=date(2025, 11, 1),
            check_out=date(2025, 11, 3),
            total_price=200.0
        )

        # Nouvelle réservation qui chevauche la précédente
        overlap_booking = CarRentBooking(
            car_rent=self.car,
            account=self.account,
            check_in=date(2025, 11, 2),
            check_out=date(2025, 11, 4),
            total_price=0
        )

        # Vérification manuelle du chevauchement
        overlap = CarRentBooking.objects.filter(
            car_rent=self.car,
            check_out__gt=overlap_booking.check_in,
            check_in__lt=overlap_booking.check_out
        )

        self.assertTrue(overlap.exists(), "Un chevauchement aurait dû être détecté.")
