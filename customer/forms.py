from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm

from .models import Customer

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

class SignUpForm(forms.Form):
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={
        'class': FORM_CONTROL_CLASS,
        'placeholder': 'Obi'
    }))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={
        'class': FORM_CONTROL_CLASS,
        'placeholder': 'Ciroma'
    }))
    email = forms.EmailField(label='Email Address', widget=forms.EmailInput(attrs={
        'class': FORM_CONTROL_CLASS,
        'placeholder': 'abc@gmail.com'
    }))
    phone_number = forms.CharField(label='Phone Number', widget=forms.TextInput(attrs={
        'class': FORM_CONTROL_CLASS,
        'placeholder': '0543334444'
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': FORM_CONTROL_CLASS,
        'placeholder': '8 characters minimum'
    }))

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if len(phone_number) > 11:
            raise ValidationError(_('Please enter phone number without spaces or country code.'))
        return phone_number

    def save(self):
        # Create user
        data = self.cleaned_data
        user = User.objects.create_user(data['email'], data['email'], data['password'])
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.save()

        # Create customer
        return Customer.objects.create(user=user, phone_number=data['phone_number'])