from django.shortcuts import render
from django.views.generic.edit import FormView

from transaction.forms import TransactionForm

class TransactionView(FormView):
    template_name = 'index.html'
    form_class = TransactionForm
    # success_url = '/thanks/'