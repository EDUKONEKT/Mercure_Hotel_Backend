from django.contrib import admin
from rooms.models import Room, RoomBooking
# Register your models here.


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display =('name','number','is_available','price')
    list_filter = ('is_available', 'name')
    search_fields = ('number',)
    exclude = ('type',) 

@admin.register(RoomBooking)
class RoomBookingAdmin(admin.ModelAdmin):
    list_display = ('room', 'account', 'check_in', 'check_out', 'total_price', 'is_deleted')
    list_filter = ('check_in', 'check_out', 'is_deleted')
    search_fields = ('room__number', 'account__user__username')
    autocomplete_fields = ['room', 'account']