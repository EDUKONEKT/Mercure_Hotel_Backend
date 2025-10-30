from django.urls import path, include
from rest_framework.routers import DefaultRouter
from meeting_room.views import MeetingRoomViewSet, MeetingRoomBookingViewSet

router = DefaultRouter()
router.register(r'meeting-room', MeetingRoomViewSet)
router.register(r'meeting-room-bookings', MeetingRoomBookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
