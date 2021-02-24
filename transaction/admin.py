from django.contrib import admin

from .models import Rates, Transaction

admin.site.register(Rates)
admin.site.register(Transaction)