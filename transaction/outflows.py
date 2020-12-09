from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.sites.models import Site

import json
import requests

def initiate_cedi_transfer(transaction, message="NGN to GHS"):
    domain = Site.objects.get_current().domain
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': '{} {}'.format('bearer', settings.ASORIBA_PUB_KEY)
    }

    data = {
        'amount': str(transaction.outflow.amount),
        'destination': transaction.outflow.dest_account_number,
        'destination_type': transaction.outflow.dest_account_provider_code,
        'metadata': {
            'user_id': transaction.user.id,
            'transaction_id': str(transaction.transaction_id)
        },
        'remarks': message,
        'post_url': '{}{}{}'.format(
            settings.PROTOCOL, domain,
            reverse_lazy('transaction:handle-cedi-transfer-update'))
    }

    payload = json.dumps(data)

    print('** Cedi transfer request **')
    print(payload)

    transfer = requests.post(
        settings.ASORIBA_TRANSFER_URL, headers=headers, data=payload).json()

    print('** Cedi transfer response **')
    print(transfer)

def initiate_naira_transfer(transaction, narration="GHS to NGN"):
    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        'account_bank': transaction.outflow.dest_account_provider_code,
        'account_number': transaction.outflow.dest_account_number,
        'amount': int(transaction.outflow.amount),
        'currency': "NGN",
        'narration': narration,
        'seckey': settings.RAVE_GH_SEC_KEY,
        'reference': transaction.transaction_id
    }

    payload = json.dumps(data)

    print('** Naira transfer request **')
    print(payload)
    
    transfer = requests.post(
        settings.FW_TRANSFER_URL, headers=headers, data=payload).json()

    print('** Naira transfer response **')
    print(transfer)
    
    transaction.outflow.reference = transfer['data']['id']
    transaction.outflow.save()