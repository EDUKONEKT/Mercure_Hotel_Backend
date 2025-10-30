from django.contrib import admin
from fitness.models import Fitness, FitnessBooking

@admin.register(Fitness)
class FitnessAdmin(admin.ModelAdmin):
    list_display = ('flour', 'number', 'max_pers', 'is_available', 'price')
    exclude = ('type',)
    list_filter = ('flour', 'is_available')
    search_fields = ('number',)

@admin.register(FitnessBooking)
class FitnessBookingAdmin(admin.ModelAdmin):
    list_display = ('fitness', 'account', 'check_in', 'check_out', 'total_price', 'is_deleted')
    list_filter = ('check_in', 'check_out', 'is_deleted')
    search_fields = ('fitness__number', 'account__user__username')
    autocomplete_fields = ['fitness', 'account']
