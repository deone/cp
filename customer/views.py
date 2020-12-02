from django.conf import settings
from django.urls import reverse_lazy
from django.utils.http import is_safe_url
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.contrib.auth import login, authenticate

from .forms import SignUpForm
from transaction.models import Rates
from transaction.forms import TransactionForm

class TransactionView(FormView):
    template_name = 'index.html'
    form_class = TransactionForm
    # success_url = '/thanks/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rates'] = Rates.objects.all()[0]
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

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

class AddAccountView(FormView):
    pass