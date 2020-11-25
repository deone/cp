from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .forms import SignInForm

app_name = 'customer'

urlpatterns = [
    path('', views.TransactionView.as_view()),
    path('sign-in', auth_views.LoginView.as_view(
        template_name='signin.html', authentication_form=SignInForm), name='sign-in'),
    path('sign-up', views.sign_up, name='sign-up'),
    path('sign-out', auth_views.LogoutView.as_view(), name='sign-out'),
]