from django.contrib import admin

from .models import (
    Rates, Transaction, Inflow, Outflow
)

admin.site.register(Rates)
admin.site.register(Inflow)
admin.site.register(Outflow)
admin.site.register(Transaction)