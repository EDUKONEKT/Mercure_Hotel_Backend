from django.contrib import admin
from sauna.models import Sauna, SaunaBooking

@admin.register(Sauna)
class SaunaAdmin(admin.ModelAdmin):
    list_display = ('price','name', 'is_available')
    list_filter = ('is_available',)
    exclude = ('type',)
    search_fields = ['price']

@admin.register(SaunaBooking)
class SaunaBookingAdmin(admin.ModelAdmin):
    list_display = ('sauna', 'account', 'check_in', 'check_out', 'total_price', 'is_deleted')
    list_filter = ('check_in', 'check_out', 'is_deleted')
    search_fields = ('sauna__id', 'account__user__username')
    autocomplete_fields = ['sauna', 'account']

# Register your models here.
