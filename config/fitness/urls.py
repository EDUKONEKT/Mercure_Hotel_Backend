from django.urls import path, include
from rest_framework.routers import DefaultRouter
from fitness.views import FitnessViewSet, FitnessBookingViewSet

router = DefaultRouter()
router.register(r'fitness', FitnessViewSet)
router.register(r'fitness-bookings', FitnessBookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
