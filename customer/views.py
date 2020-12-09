from django.views import View
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.http import is_safe_url
from django.contrib.sites.models import Site
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic.base import ContextMixin
from django.contrib.auth import login, authenticate

from .forms import SignUpForm
from transaction import inflows
from customer.models import RecipientAccount
from transaction.models import Rates, Transaction
from transaction.forms import (
    TransactionForm, MobileMoneyWalletForm, BankAccountForm
)

class TransactionView(FormView):
    template_name = 'index.html'
    form_class = TransactionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rates'] = Rates.objects.all()[0]
        return context

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('customer:add-account', kwargs={'transaction_id': self.object.transaction_id})

class SignUpView(FormView):
    template_name = 'signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('customer:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', '')
        return context

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get('email')
        raw_password = form.cleaned_data.get('password')

        # Authenticate and log user in
        user = authenticate(username=email, password=raw_password)
        login(self.request, user)

        # get the redirect location
        redirect_to = self.request.GET.get('next', '')
        url_is_safe = is_safe_url(redirect_to, settings.ALLOWED_HOSTS)
        if redirect_to and url_is_safe:
            return redirect(redirect_to)
        return super().form_valid(form)

class AddAccountView(View, ContextMixin):
    template_name = 'transaction/add-account.html'
    outflow_currency_form_map = {
        'GHS': MobileMoneyWalletForm,
        'NGN': BankAccountForm
    }

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.customer = request.user.customer
        self.transaction = Transaction.objects.get(
            transaction_id=kwargs.get('transaction_id'))
        self.outflow_currency = self.transaction.outflow.currency
        self.form_args = {
            'customer': self.customer,
            'transaction': self.transaction
        }

    def _get_account_type(self, form):
        if isinstance(form, MobileMoneyWalletForm):
            return 'wallet'
        return 'bank'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'site': '{}{}'.format(settings.PROTOCOL, Site.objects.get_current()),
            'accounts': RecipientAccount.objects.filter(
                _type=self._get_account_type(self.form), customer=self.customer),
            'form': self.form,
            'beneficiary_url': settings.FW_CREATE_BENEFICIARY_URL,
            'currency': self.outflow_currency,
        })
        return context

    def get(self, request, *args, **kwargs):
        self.form = self.outflow_currency_form_map[self.outflow_currency](**self.form_args)
        response = render(request, self.template_name, self.get_context_data(**kwargs))
        response.set_cookie('key', value=settings.FW_INCISIA_SEC_KEY)
        return response

    def post(self, request, *args, **kwargs):
        self.form = self.outflow_currency_form_map[self.outflow_currency](request.POST, **self.form_args)
        if self.form.is_valid():
            self.form.save()
            # redirect to confirmation page.
            return redirect(reverse_lazy('customer:confirm-transaction', kwargs={
                'transaction_id': self.transaction.transaction_id}))
        return render(request, self.template_name, self.get_context_data(**kwargs))

class ConfirmTransactionView(View, ContextMixin):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.customer = request.user.customer
        self.transaction = Transaction.objects.get(
            transaction_id=kwargs.get('transaction_id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'transaction': self.transaction,
        })
        return context

    def get(self, request, *args, **kwargs):
        return render(request, 'transaction/confirm.html', self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):
        site = Site.objects.get_current().domain
        transaction_id = self.transaction.transaction_id
        amount = self.transaction.inflow.amount

        if self.transaction.inflow.currency == 'NGN':
            redirect_url = '{}{}{}'.format(
                settings.PROTOCOL, site,
                reverse_lazy('transaction:save-naira-payment-info'))
            payment_page = inflows.get_naira_payment_page(
                request.user.email, transaction_id, int(amount), redirect_url)
            return redirect(payment_page)

        redirect_url = '{}{}{}'.format(
            settings.PROTOCOL, site,
            reverse_lazy('transaction:save-cedi-payment-info'))
        post_url = '{}{}{}'.format(
            settings.PROTOCOL, site,
            reverse_lazy('transaction:handle-cedi-payment-update'))
        payment_page = inflows.get_cedi_payment_page(
            request.user.email, transaction_id, int(amount), redirect_url, post_url)
        return redirect(payment_page)


class GetAccountsView(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '')
        _type = request.GET.get('type', '')

        if q != '':
            # if q is numeric, search by number
            try:
                int(q)
            except ValueError:
                accounts = list(RecipientAccount.objects.filter(
                    _type=_type, customer=request.user.customer, name__icontains=q).values())
            else:
                accounts = list(RecipientAccount.objects.filter(
                    _type=_type, customer=request.user.customer, number__icontains=q).values())
        else:
            accounts = list(RecipientAccount.objects.filter(
                _type=_type, customer=request.user.customer).values())

        return JsonResponse(accounts, safe=False)