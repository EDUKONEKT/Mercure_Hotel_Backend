from django.contrib import admin
from car_rent.models import Car_rent, CarRentBooking
# Register your models here.


@admin.register(Car_rent)
class CarRentAdmin(admin.ModelAdmin):
    list_display = ('name', 'qty', 'is_available', 'price')
    exclude = ('type',)
    list_filter = ('is_available', 'name')
    search_fields = ('name',)

@admin.register(CarRentBooking)
class CarRentBookingAdmin(admin.ModelAdmin):
    list_display = ('car_rent', 'account', 'check_in', 'check_out', 'total_price', 'is_deleted')
    list_filter = ('check_in', 'check_out', 'is_deleted')
    search_fields = ('car_rent__name', 'account__user__username')
    autocomplete_fields = ['car_rent', 'account']
 
