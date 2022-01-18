from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from . import SOURCE_CURRENCIES, DEST_CURRENCIES

from decimal import Decimal

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

    def __str__(self):
        return '{}{}{}'.format(self.transaction_id, ', ', self.is_complete)

class Flow(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    fee = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    reference = models.CharField(max_length=50, null=True, blank=True)
    updated_at = models.DateTimeField(default=timezone.now)
    is_complete = models.BooleanField(default=False)

    class Meta:
        abstract = True
        ordering = ['-updated_at']

class Inflow(Flow):
    usd_value = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    usd_paid = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    source_account_provider = models.CharField(max_length=50, null=True, blank=True)
    source_account_number = models.CharField(max_length=50, null=True, blank=True)
    source_account_name = models.CharField(max_length=100, null=True, blank=True)
    currency = models.CharField(max_length=3, choices=SOURCE_CURRENCIES)

    def __str__(self):
        return '{}{}{}{}{}{}'.format(
            self.transaction.transaction_id, ' - ', self.currency, self.amount, ', ', self.is_complete)

class Outflow(Flow):
    dest_account_provider_code = models.CharField(max_length=15, null=True, blank=True)
    dest_account_provider_name = models.CharField(max_length=50, null=True, blank=True)
    dest_account_number = models.CharField(max_length=20, null=True, blank=True)
    dest_account_name = models.CharField(max_length=50, null=True, blank=True)
    currency = models.CharField(max_length=3, choices=DEST_CURRENCIES)

    def __str__(self):
        return '{}{}{}{}{}{}'.format(
            self.transaction.transaction_id, ' - ', self.currency, self.amount, ', ', self.is_complete)

class Rates(models.Model):
    ngn_to_ghs = models.DecimalField(max_digits=8, decimal_places=5)
    ghs_to_ngn = models.DecimalField(max_digits=8, decimal_places=5)
    btc_to_ngn = models.DecimalField(max_digits=15, decimal_places=2)
    btc_to_ghs = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{}, {}, {}, {}'.format(
            self.ngn_to_ghs, self.ghs_to_ngn, self.btc_to_ngn, self.btc_to_ghs)

    class Meta:
        ordering = ['-date_created']
        verbose_name_plural = 'Rates'

INFLOW_FEE = {
    'GHS': 0.02,
    'NGN': 0.025,
    'BTC': 0.01
}

OUTFLOW_FEE = {
    'GHS': 0.01
}

def get_naira_outflow_fee(amount):
    if amount < Decimal(5001):
        return Decimal(10.75)
    elif amount > Decimal(5000) and amount < Decimal(50001):
        return Decimal(26.88)
    elif amount > Decimal(50000):
        return Decimal(53.75)

class Report(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    transaction_id = models.CharField(max_length=30, unique=True)
    inflow_currency = models.CharField(max_length=3, choices=SOURCE_CURRENCIES)
    inflow_amount = models.DecimalField(max_digits=14, decimal_places=2)
    inflow_fee = models.DecimalField(max_digits=10, decimal_places=2) # payment_receiving_fee_percentage * inflow_amount
    outflow_currency = models.CharField(max_length=3, choices=SOURCE_CURRENCIES)
    outflow_amount = models.DecimalField(max_digits=14, decimal_places=2)
    outflow_fee = models.DecimalField(max_digits=10, decimal_places=2)
    outflow_amount_value = models.DecimalField(max_digits=14, decimal_places=2) # (nnamdi/google rate ( = rate / 0.95) * inflow_amount)
    revenue_currency = models.CharField(max_length=3, choices=SOURCE_CURRENCIES)
    revenue = models.DecimalField(max_digits=10, decimal_places=2) # (outflow_amount_value - outflow_amount)

    def __str__(self):
        return self.transaction_id