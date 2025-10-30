from django.db import models
from accounts.models import Account

class AbstractBooking(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE,null=True, blank=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
