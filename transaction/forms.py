from django import forms

from . import CURRENCIES

FORM_CONTROL_CLASS = 'form-control'

class TransactionForm(forms.Form):
    source_amount = forms.CharField(label='You send', widget=forms.TextInput(attrs={
        'class': '{} {}'.format('autonumeric', FORM_CONTROL_CLASS)
    }))
    source_currency = forms.ChoiceField(label='Currency I have', widget=forms.Select(attrs={
        'class': FORM_CONTROL_CLASS
    }), choices=CURRENCIES)
    dest_amount = forms.CharField(label='Recipient gets', widget=forms.TextInput(attrs={
        'class': FORM_CONTROL_CLASS
    }))
    dest_currency = forms.ChoiceField(label="Recipient's currency", widget=forms.Select(attrs={
        'class': FORM_CONTROL_CLASS
    }), choices=CURRENCIES)