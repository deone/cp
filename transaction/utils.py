from django.conf import settings
from django.utils import timezone

import math
import requests
from decimal import Decimal

NETWORKS = [
    ('mtn', 'MTN'),
    ('vodafone', 'Vodafone'),
    ('airtel', 'AirtelTigo'),
]

def get_transaction_id(ref):
    if '_' in ref:
        return ref.split('_')[0]
    return ref

def update_inflow(inflow, **data):
    inflow.fee = data.get('fee', None)
    inflow.reference = data.get('reference', None)
    inflow.usd_paid = data.get('usd_paid', None)
    inflow.source_account_provider = data.get('source_account_provider', None)
    inflow.source_account_number = data.get('source_account_number', None)
    inflow.source_account_name = data.get('source_account_name', None)

    inflow.updated_at = timezone.now()
    if data.get('is_complete', None):
        inflow.is_complete = True
    inflow.save()

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
    return '{}{}'.format('TMNY', timezone.now().strftime('%y%m%d%H%M%S%f'))

def get_banks():
    # Get json from API
    # Catch requests.exceptions.ConnectionError here
    try:
        r = requests.get('{}{}{}{}'.format(
            settings.FW_BANKS_URL, 'NG', '?public_key=', settings.FW_INCISIA_PUB_KEY))
    except requests.exceptions.ConnectionError:
        return [('', 'Unable to fetch banks. Please retry shortly.')]
    else:
        if r.status_code == 200:
            json = r.json()['data']['Banks']
            lst = [(a['Code'], a['Name']) for a in json]
            banks = [('', 'Select Bank')] + lst
            return banks
        else:
            # display message as form error, if possible
            pass