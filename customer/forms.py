from django import forms
from django.contrib.auth.forms import AuthenticationForm

FORM_CONTROL_CLASS = 'form-control'

class SignInForm(AuthenticationForm):
    # Validate this as email address
    username = forms.CharField(label='Email Address', widget=forms.EmailInput(attrs={
        'class': FORM_CONTROL_CLASS,
        'placeholder': 'abc@gmail.com',
        'autofocus': True
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': FORM_CONTROL_CLASS,
        'placeholder': 'Enter Password'
    }))