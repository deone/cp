from django.conf import settings

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

    payment = requests.post(
        settings.ASORIBA_PAYMENT_URL, headers=headers, data=payload)

    return payment.json()['url']

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