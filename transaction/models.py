from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from . import SOURCE_CURRENCIES, DEST_CURRENCIES

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    transaction_id = models.CharField(max_length=30, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, default='Pending') # we only really need this for cancelled transactions
    is_complete = models.BooleanField(default=False) # Use this as transaction status

    class Meta:
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('customer:transaction-detail', kwargs={'pk': self.pk})

class Flow(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=14, decimal_places=5)
    reference = models.CharField(max_length=50, null=True)
    updated_at = models.DateTimeField(default=timezone.now)
    is_complete = models.BooleanField(default=False)

    class Meta:
        abstract = True
        ordering = ['-updated_at']

class Inflow(Flow):
    source_account_provider = models.CharField(max_length=50, null=True)
    source_account_number = models.CharField(max_length=20, null=True)
    source_account_name = models.CharField(max_length=50, null=True)
    currency = models.CharField(max_length=3, choices=SOURCE_CURRENCIES)

class Outflow(Flow):
    dest_account_provider_code = models.CharField(max_length=15, null=True)
    dest_account_provider_name = models.CharField(max_length=50, null=True)
    dest_account_number = models.CharField(max_length=20, null=True)
    dest_account_name = models.CharField(max_length=50, null=True)
    currency = models.CharField(max_length=3, choices=DEST_CURRENCIES)

class Rates(models.Model):
    ngn_to_ghs = models.DecimalField(max_digits=8, decimal_places=5)
    ghs_to_ngn = models.DecimalField(max_digits=8, decimal_places=5)
    btc_to_ngn = models.DecimalField(max_digits=15, decimal_places=2)
    btc_to_ghs = models.DecimalField(max_digits=10, decimal_places=2)