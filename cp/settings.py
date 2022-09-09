"""
Django settings for cp project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

import os
import dotenv
dotenv.read_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'customer.apps.CustomerConfig',
    'transaction.apps.TransactionConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cp_dev',
        'USER': 'cp_admin',
        'PASSWORD': os.environ['DEV_DB_PASSWORD'],
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

# My settings
SITE_ID = 1

PROTOCOL = 'http://'

STATICFILES_DIRS = (
    BASE_DIR / 'static',
)

LOGIN_URL = '/sign-in'

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/'

# Flutterwave
FW_INCISIA_SEC_KEY = os.environ['FW_INCISIA_DEV_SEC_KEY']
FW_INCISIA_PUB_KEY = os.environ['FW_INCISIA_DEV_PUB_KEY']

FW_TRANSFER_URL = 'https://api.ravepay.co/v2/gpx/transfers/create'
FW_BANKS_URL = 'https://api.ravepay.co/v2/banks/'
FW_CREATE_BENEFICIARY_URL = 'https://api.ravepay.co/v2/gpx/transfers/beneficiaries/create'
FW_PAYMENT_URL = 'https://api.ravepay.co/flwv3-pug/getpaidx/api/v2/hosted/pay'

# Asoriba
ASORIBA_PUB_KEY = os.environ['ASORIBA_DEV_PUB_KEY']
ASORIBA_PAYMENT_URL = 'https://sandbox.mybusinesspay.com//payment/v1.0/initialize'
ASORIBA_TRANSFER_URL = 'https://sandbox.mybusinesspay.com//payment/v1.0.1/payouts'

# Opennode
OPENNODE_API_KEY = os.environ['OPENNODE_DEV_API_KEY']
OPENNODE_CREATE_CHARGE_URL = 'https://dev-api.opennode.co/v1/charges'
OPENNODE_CHECKOUT_URL = 'https://dev-checkout.opennode.co/'
OPENNODE_MAX_TRANSFER_AMOUNT = 0.042

# Email
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_PORT = 587
EMAIL_USE_TLS = True

MARGIN = '0.05'
BTC_MARGIN = '0.0248'