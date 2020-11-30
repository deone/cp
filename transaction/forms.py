from django import forms

from . import SOURCE_CURRENCIES, DEST_CURRENCIES

FORM_CONTROL_CLASS = 'form-control'

class TransactionForm(forms.Form):
    source_amount = forms.CharField(label='You send', widget=forms.TextInput(attrs={
        'class': FORM_CONTROL_CLASS,
        'id': 'source_amount',
        'autofocus': True,
        'value': '1000',
    }))
    source_currency = forms.ChoiceField(label='Currency I have', widget=forms.Select(attrs={
        'class': FORM_CONTROL_CLASS
    }), choices=SOURCE_CURRENCIES)
    dest_amount = forms.CharField(label='Recipient gets', widget=forms.TextInput(attrs={
        'class': FORM_CONTROL_CLASS,
        'id': 'dest_amount',
    }))
    dest_currency = forms.ChoiceField(label="Recipient's currency", widget=forms.Select(attrs={
        'class': FORM_CONTROL_CLASS,
    }), choices=DEST_CURRENCIES)