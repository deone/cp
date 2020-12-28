from django import template

from decimal import Decimal

register = template.Library()

@register.filter
def sats_to_btc(sats):
    return Decimal(sats / 100000000)