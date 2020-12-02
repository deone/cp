from django.utils import timezone

import math
from decimal import Decimal

def get_dest_currency(data, source_currency):
    dest_currency = data.get('dest_currency', None)
    if dest_currency is None:
        if source_currency == 'NGN':
            return 'GHS'
        return 'NGN'
    return dest_currency

def get_amount(string, currency):
    if currency == 'GHS':
        amount_string = string[3:]
    else:
        amount_string = string[1:]
    return amount_string.replace(',', '')

def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(Decimal(n)*multiplier + Decimal(0.5) / multiplier)

def create_transaction_id():
    return '{}{}'.format('CSHP', timezone.now().strftime('%y%m%d%H%M%S'))