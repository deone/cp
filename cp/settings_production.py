from cp.settings import *

import os

DEBUG = False

ADMINS = [('Dayo Osikoya', 'alwaysdeone@gmail.com')]

ALLOWED_HOSTS = [
    'transfr.money',
    'www.transfr.money'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cp',
        'USER': 'cp_admin',
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}

STATIC_ROOT = '/home/sdarko/webapps/cashpipe_static'

# Flutterwave
FW_INCISIA_SEC_KEY = os.environ['FW_INCISIA_PROD_SEC_KEY']
FW_INCISIA_PUB_KEY = os.environ['FW_INCISIA_PROD_PUB_KEY']

FW_TRANSFER_URL = 'https://api.ravepay.co/v2/gpx/transfers/create'
FW_BANKS_URL = 'https://api.ravepay.co/v2/banks/'
FW_CREATE_BENEFICIARY_URL = 'https://api.ravepay.co/v2/gpx/transfers/beneficiaries/create'
FW_PAYMENT_URL = 'https://api.ravepay.co/flwv3-pug/getpaidx/api/v2/hosted/pay'

# Opennode
OPENNODE_API_KEY = os.environ['OPENNODE_PROD_API_KEY']
OPENNODE_CREATE_CHARGE_URL = 'https://api.opennode.co/v1/charges'
OPENNODE_CHECKOUT_URL = 'https://checkout.opennode.co/'
OPENNODE_MAX_TRANSFER_AMOUNT = 0.042

# Asoriba
ASORIBA_PUB_KEY = os.environ['ASORIBA_PROD_PUB_KEY']
ASORIBA_PAYMENT_URL = 'https://app.mybusinesspay.com//payment/v1.0/initialize'
ASORIBA_TRANSFER_URL = 'https://app.mybusinesspay.com//payment/v1.0.1/payouts'