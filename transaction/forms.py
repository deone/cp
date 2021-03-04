from django import forms

from .utils import *
from customer.models import RecipientAccount
from . import SOURCE_CURRENCIES, DEST_CURRENCIES
from .models import (Transaction, Inflow, Outflow)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from decimal import Decimal
import requests
import copy

FORM_CONTROL_CLASS = 'form-control'

class TransactionForm(forms.Form):
    source_amount = forms.CharField(label='You send', widget=forms.TextInput(attrs={
        'class': FORM_CONTROL_CLASS,
        'autofocus': True,
        'value': '1000',
    }))
    source_currency = forms.ChoiceField(label='Currency I have', widget=forms.Select(attrs={
        'class': 'form-select'
    }), choices=SOURCE_CURRENCIES)
    dest_amount = forms.CharField(label='Recipient gets', widget=forms.TextInput(attrs={
        'class': FORM_CONTROL_CLASS,
        'readonly': True
    }))
    dest_currency = forms.ChoiceField(label="Recipient's currency", widget=forms.Select(attrs={
        'class': 'form-select',
    }), choices=DEST_CURRENCIES)

    def clean_source_amount(self):
        return Decimal(self.cleaned_data['source_amount'].replace(',', ''))

    def clean_source_currency(self):
        if self.cleaned_data['source_currency'] == 'BTC':
            # Get BTC value of amount specified in USD
            data = requests.get('https://api.opennode.com/v1/rates')
            if data.status_code == 200:
                amount = data.json()['data']['BTCUSD']['USD']
                btc_value = self.cleaned_data['source_amount'] / Decimal(amount)
                return self.cleaned_data['source_currency'], btc_value
            else:
                raise ValidationError('Unfortunately, we are unable to get BTC value. Please try again later.')
        return self.cleaned_data['source_currency']

    def clean_dest_amount(self):
        dest_amount = self.cleaned_data['dest_amount']
        if dest_amount.startswith('G'):
            return round(Decimal(get_amount(dest_amount, 'GHS')), 2)
        return Decimal(round_half_up(get_amount(dest_amount, 'NGN')))

    def save(self):
        # Create transaction
        transaction = Transaction.objects.create(transaction_id=create_transaction_id())

        # Check source currency - we get a tuple if source currency is BTC
        if isinstance(self.cleaned_data['source_currency'], str):
            source_currency = self.cleaned_data['source_currency']
        else:
            source_currency, btc_value = self.cleaned_data['source_currency']
        source_amount = self.cleaned_data['source_amount']

        # Create inflow
        inflow_data = {
            'transaction': transaction,
            'currency': source_currency,
        }

        if source_currency == 'BTC':
            inflow_data.update({
                'usd_value': source_amount,
                'amount': round_half_up(btc_value * 100000000) # in satoshis
            })
        else:
            inflow_data.update({
                'amount': source_amount
            })

        inflow = Inflow(**inflow_data)
        inflow.save()

        # Create outflow
        outflow_data = {
            'transaction': transaction,
            'amount': self.cleaned_data['dest_amount'],
            'currency': self.cleaned_data['dest_currency']
        }

        outflow = Outflow(**outflow_data)
        outflow.save()

        return transaction

class AccountForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.customer = kwargs.pop('customer')
        self.transaction = kwargs.pop('transaction')
        super().__init__(*args, **kwargs)

    def clean_number(self):
        number = self.cleaned_data['number']
        if len(number) != 10:
            raise ValidationError(_('Number is either incomplete or too long.'))
        return self.cleaned_data['number']

    class Meta:
        model = RecipientAccount
        fields = (
            'provider_code',
            'provider_name',
            'number',
        )
        widgets = {
            'provider_name': forms.HiddenInput(),
        }

class MobileMoneyWalletForm(AccountForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['provider_code'].label='Wallet Provider'
        self.fields['number'].label = 'Phone Number'

    class Meta(AccountForm.Meta):
        fields = ['confirm_number']
        fields.extend(AccountForm.Meta.fields)

        widgets = copy.deepcopy(AccountForm.Meta.widgets)
        widgets.update({
            'provider_code': forms.Select(
                choices=NETWORKS, attrs={'class': 'form-select'}),
            'number': forms.TextInput(
                attrs={'class': FORM_CONTROL_CLASS, 'placeholder': '0500002214'}),
            'confirm_number': forms.TextInput(
                attrs={'class': FORM_CONTROL_CLASS, 'placeholder': '0500002214'})
        })

    def clean_number(self):
        number = self.cleaned_data['number']
        confirm_number = self.cleaned_data['confirm_number']
        if number != confirm_number:
            raise ValidationError(_('Phone numbers do not match. Please enter matching numbers.'))
        return self.cleaned_data['number']

    def save(self):
        return add_account('wallet', self.customer, self.transaction, **self.cleaned_data)

def add_account(account_type, customer, transaction, **data):
    # Save account if it doesn't exist
    d = copy.deepcopy(data)
    d.update({
        '_type': account_type,
        'customer': customer
    })
    try:
        account = RecipientAccount.objects.get(
            _type=account_type, number=d['number'], customer=customer)
    except RecipientAccount.DoesNotExist:
        account = RecipientAccount.objects.create(**d)

    # Update transaction with user
    transaction.user = customer.user
    transaction.save()

    # Update transaction outflow with recipient account details
    outflow = transaction.outflow
    outflow.dest_account_provider_code = data.get('provider_code', None)
    outflow.dest_account_provider_name = data.get('provider_name', None)
    outflow.dest_account_number = data.get('number', None)
    outflow.dest_account_name = data.get('name', None)
    outflow.save()

    return account

class BankAccountForm(AccountForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['provider_code'].label='Bank'
        self.fields['number'].label = 'Account Number'
        self.fields['name'].label = 'Account Name'

    class Meta(AccountForm.Meta):
        fields = ['name']
        fields.extend(AccountForm.Meta.fields)

        widgets = copy.deepcopy(AccountForm.Meta.widgets)
        widgets.update({
            'number': forms.TextInput(
                attrs={'class': FORM_CONTROL_CLASS, 'placeholder': '0110000221'}),
            'provider_code': forms.Select(
                choices=get_banks(), attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': FORM_CONTROL_CLASS, 'readonly': True})
        })

    def save(self):
        return add_account('bank', self.customer, self.transaction, **self.cleaned_data)