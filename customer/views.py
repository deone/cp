from django.urls import reverse_lazy
from django.utils.http import is_safe_url
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.contrib.auth import login, authenticate

from .forms import SignUpForm
from transaction.forms import TransactionForm

class TransactionView(FormView):
    template_name = 'index.html'
    form_class = TransactionForm
    # success_url = '/thanks/'

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')

            # Authenticate and log user in
            user = authenticate(username=email, password=raw_password)
            login(request, user)

            # get the redirect location
            redirect_to = request.GET.get('next', '')
            url_is_safe = is_safe_url(redirect_to, settings.ALLOWED_HOSTS)
            if redirect_to and url_is_safe:
                return redirect(redirect_to)
            return redirect(reverse_lazy('customer:index'))
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {
        'form': form, 'next': request.GET.get('next', '')})