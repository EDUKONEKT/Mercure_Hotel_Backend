from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarRentViewSet ,CarRentBookingViewSet

router = DefaultRouter()
router.register(r'car_rent', CarRentViewSet)
router.register(r'car_rent_bookings', CarRentBookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
