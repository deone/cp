from django import forms

from .utils import *
from customer.models import RecipientAccount
from . import SOURCE_CURRENCIES, DEST_CURRENCIES
from .models import (Transaction, Inflow, Outflow)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from decimal import Decimal
import copy

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

    def clean_source_amount(self):
        return Decimal(self.cleaned_data['source_amount'].replace(',', ''))

    def clean_dest_amount(self):
        dest_amount = self.cleaned_data['dest_amount']
        if dest_amount.startswith('G'):
            return round(Decimal(get_amount(dest_amount, 'GHS')), 2)
        return Decimal(round_half_up(get_amount(dest_amount, 'NGN')))

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
                choices=NETWORKS, attrs={'class': FORM_CONTROL_CLASS}),
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
    update_outflow(outflow, d)

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
                choices=get_banks(), attrs={'class': FORM_CONTROL_CLASS}),
            'name': forms.TextInput(attrs={'class': FORM_CONTROL_CLASS, 'readonly': True})
        })

    def save(self):
        return add_account('bank', self.customer, self.transaction, **self.cleaned_data)