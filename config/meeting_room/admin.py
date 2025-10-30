from django.contrib import admin
from meeting_room.models import MeetingRoom, MeetingRoomBooking

@admin.register(MeetingRoom)
class MeetingRoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'flour', 'max_pers', 'is_available', 'price')
    exclude = ('type',)
    list_filter = ('is_available', 'flour')
    search_fields = ('number',)

@admin.register(MeetingRoomBooking)
class MeetingRoomBookingAdmin(admin.ModelAdmin):
    list_display = ('meeting_room', 'account', 'date', 'start_time', 'end_time', 'total_price', 'is_deleted')
    list_filter = ('date', 'is_deleted')
    search_fields = ('meeting_room__number', 'account__user__username')
    autocomplete_fields = ['meeting_room', 'account']
