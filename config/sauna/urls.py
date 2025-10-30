from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sauna.views import SaunaViewSet, SaunaBookingViewSet

router = DefaultRouter()
router.register(r'saunas', SaunaViewSet)
router.register(r'sauna-bookings', SaunaBookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
