from django.contrib import admin

from .models import (
    Rates, Transaction, Inflow, Outflow, Report
)

admin.site.register(Rates)
admin.site.register(Inflow)
admin.site.register(Report)
admin.site.register(Outflow)
admin.site.register(Transaction)