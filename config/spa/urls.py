from django.urls import path, include
from rest_framework.routers import DefaultRouter
from spa.views import SpaViewSet, SpaBookingViewSet

router = DefaultRouter()
router.register(r'spas', SpaViewSet)
router.register(r'spa-bookings', SpaBookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
