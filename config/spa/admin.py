from django.contrib import admin
from spa.models import Spa, SpaBooking

@admin.register(Spa)
class SpaAdmin(admin.ModelAdmin):
    list_display = ('price','name', 'is_available')
    exclude = ('type',)
    search_fields = ['price','name']

@admin.register(SpaBooking)
class SpaBookingAdmin(admin.ModelAdmin):
    list_display = ('spa', 'account', 'check_in', 'check_out', 'total_price', 'is_deleted')
    list_filter = ('check_in', 'check_out', 'is_deleted')
    search_fields = ('spa__id', 'account__user__username')
    autocomplete_fields = ['spa', 'account']

# Register your models here.
