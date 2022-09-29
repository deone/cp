from django import forms
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm

from .models import Customer

FIELD_CLASS = 'form-control'

class SignInForm(AuthenticationForm):
    # Validate this as email address
    username = forms.CharField(label='Email Address', widget=forms.EmailInput(attrs={
        'class': FIELD_CLASS,
        'placeholder': 'abc@gmail.com',
        'autofocus': True
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': FIELD_CLASS,
        'placeholder': 'Enter Password'
    }))

class SignUpForm(forms.Form):
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={
        'class': FIELD_CLASS,
        'placeholder': 'Obi'
    }))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={
        'class': FIELD_CLASS,
        'placeholder': 'Ciroma'
    }))
    email = forms.EmailField(label='Email Address', widget=forms.EmailInput(attrs={
        'class': FIELD_CLASS,
        'placeholder': 'abc@gmail.com'
    }))
    phone_number = forms.CharField(label='Phone Number', widget=forms.TextInput(attrs={
        'class': FIELD_CLASS,
        'placeholder': '0543334444'
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': FIELD_CLASS,
        'placeholder': '8 characters minimum'
    }))

    def clean(self):
        email = self.cleaned_data['email']
        try:
            u = User.objects.get(username=email)
        except IntegrityError:
            pass
        else:
            from django.utils.safestring import mark_safe
            message = mark_safe('{} {}'.format(
                'Looks like you already have an account. Please',
                '<a href="/sign-in">log in.</a>'
            ))
            raise ValidationError(
                _(message),
                code='account-exists'
            )

    def save(self):
        # Create user
        data = self.cleaned_data
        user = User.objects.create_user(data['email'], data['email'], data['password'])
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.save()

        # Create customer
        return Customer.objects.create(user=user, phone_number=data['phone_number'])

class TPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_('Email'),
        max_length=254,
        widget=forms.EmailInput(attrs={
            'autocomplete': 'email', 'placeholder': 'Email address', 'class': FIELD_CLASS, 'autofocus': True})
    )

class TSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_('New password'),
        widget=forms.PasswordInput(attrs={
            'placeholder': 'New password', 'autocomplete': 'new-password', 'class': FIELD_CLASS}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_('New password confirmation'),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'New password (again)', 'autocomplete': 'new-password', 'class': FIELD_CLASS}),
    )