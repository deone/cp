from django import forms

from .utils import *
from . import SOURCE_CURRENCIES, DEST_CURRENCIES
from .models import (Transaction, Inflow, Outflow)

from decimal import Decimal

FORM_CONTROL_CLASS = 'form-control'

class TransactionForm(forms.Form):
    source_amount = forms.CharField(label='You send', widget=forms.TextInput(attrs={
        'class': FORM_CONTROL_CLASS,
        'autofocus': True,
        'value': '1000',
    }))
    source_currency = forms.ChoiceField(label='Currency I have', widget=forms.Select(attrs={
        'class': FORM_CONTROL_CLASS
    }), choices=SOURCE_CURRENCIES)
    dest_amount = forms.CharField(label='Recipient gets', widget=forms.TextInput(attrs={
        'class': FORM_CONTROL_CLASS,
        'readonly': True
    }))
    dest_currency = forms.ChoiceField(label="Recipient's currency", widget=forms.Select(attrs={
        'class': FORM_CONTROL_CLASS,
    }), choices=DEST_CURRENCIES)

    def clean_dest_amount(self):
        dest_currency = get_dest_currency(
            self.cleaned_data, self.cleaned_data['source_currency'])

        if dest_currency == 'NGN':
            # Round to nearest whole number
            # if destination currency is Naira
            dest_amount = get_amount(self.cleaned_data['dest_amount'], 'NGN')
            return Decimal(round_half_up(dest_amount))

        # Round to 2 decimal places if destination
        # currency is Cedi
        dest_amount = get_amount(self.cleaned_data['dest_amount'], 'GHS')
        return round(Decimal(dest_amount), 2)

    def clean_source_amount(self):
        return Decimal(self.cleaned_data['source_amount'].replace(',', ''))

    def save(self):
        # Create transaction
        transaction = Transaction.objects.create(transaction_id=create_transaction_id())

        # Create inflow
        inflow_data = {
            'transaction': transaction,
            'amount': self.cleaned_data['source_amount'],
            'currency': self.cleaned_data['source_currency'],
        }

        inflow = Inflow(**inflow_data)
        inflow.save()

        # Create outflow
        outflow_data = {
            'transaction': transaction,
            'amount': self.cleaned_data['dest_amount'],
            'currency': get_dest_currency(
                self.cleaned_data, self.cleaned_data['dest_currency'])
        }

        outflow = Outflow(**outflow_data)
        outflow.save()

        return transaction