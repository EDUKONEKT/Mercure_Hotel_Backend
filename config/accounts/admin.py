from django.contrib import admin
from accounts.models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('type', 'user', 'user_email', 'user_full_name')

    def user_email(self, obj):
        return obj.user.email

    def user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    search_fields = ['user__username', 'user__email']