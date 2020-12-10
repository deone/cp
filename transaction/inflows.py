from django.conf import settings
from django.utils import timezone
from django.urls import reverse_lazy

import json
import requests

def get_cedi_payment_page(email, transaction_id, amount, redirect_url, post_url):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': '{} {}'.format('bearer', settings.ASORIBA_PUB_KEY)
    }

    data = {
        "amount": amount,
        "metadata": {
            "order_id": transaction_id,
            "product_name": "Money transfer",
            "product_description": "GHS to NGN"
        },
        "callback": redirect_url,
        "post_url": post_url,
        "email": email
    }

    payload = json.dumps(data)

    print('** Cedi payment page request **')
    print(payload)

    payment_page = requests.post(
        settings.ASORIBA_PAYMENT_URL, headers=headers, data=payload)

    print('** Cedi payment page response **')
    print(payment_page)

    return payment_page.json()['url']

def get_naira_payment_page(email, transaction_id, amount, redirect_url):
    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        "PBFPubKey": settings.FW_INCISIA_PUB_KEY,
        "amount": amount,
        "customer_email": email,
        "currency": "NGN",
        "txref": transaction_id,
        "redirect_url": redirect_url,
        "payment_options": "card,bank transfer"
    }

    payload = json.dumps(data)

    print('** Naira payment page request **')
    print(payload)

    payment_page = requests.post(
        settings.FW_PAYMENT_URL, headers=headers, data=payload)

    print('** Naira payment page response **')
    print(payment_page.json())

    return payment_page.json()['data']['link']

def get_invoice(user, transaction, domain):
    data = {
        "amount": int(transaction.inflow.amount),
        "description": "{} {} {}".format(
            'BTC', 'to', transaction.outflow.currency),
        "order_id": transaction.transaction_id,
        "customer_name": user.get_full_name(),
        "customer_email": user.username,
        "callback_url": "{}{}{}".format(
            settings.PROTOCOL, domain, reverse_lazy('transaction:handle-BTC-payment-update')),
        "success_url": "{}{}{}".format(
            settings.PROTOCOL, domain, reverse_lazy('customer:index')),
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': settings.OPENNODE_API_KEY,
    }

    charge_payload = json.dumps(data)

    print('** BTC invoice request **')
    print(charge_payload)

    charge = requests.post(
        settings.OPENNODE_CREATE_CHARGE_URL, headers=headers, data=charge_payload)

    print('** BTC invoice response **')
    print(charge.json())

    return '{}{}'.format(settings.OPENNODE_CHECKOUT_URL, charge.json()['data']['id'])