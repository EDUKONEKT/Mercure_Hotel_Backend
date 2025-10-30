from django.urls import path, include
from rest_framework.routers import DefaultRouter
from restaurant.views import MealViewSet, MealBookingViewSet

router = DefaultRouter()
router.register(r'meals', MealViewSet)
router.register(r'meal-bookings', MealBookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
