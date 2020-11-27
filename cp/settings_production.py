from ex.settings import *

import os

DEBUG = False

ADMINS = [('Dayo Osikoya', 'alwaysdeone@gmail.com')]

ALLOWED_HOSTS = [
    'cashpipe.africa',
    'www.cashpipe.africa'
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