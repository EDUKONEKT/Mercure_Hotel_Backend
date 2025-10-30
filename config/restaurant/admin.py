from django.contrib import admin
from restaurant.models import Meal, MealBooking
# Register your models here.

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('meal_type','price')
    exclude = ('type',)
    list_filter = ('meal_type', 'is_available')
    search_fields = ['meal_type']

@admin.register(MealBooking)
class MealBookingAdmin(admin.ModelAdmin):
    list_display = ('meal', 'quantity', 'account', 'total_price', 'created_at', 'is_deleted')
    list_filter = ('meal__meal_type',)
    search_fields = ('account__user__username',)
    autocomplete_fields = ['meal', 'account']
