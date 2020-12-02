from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from . import views
from .forms import SignInForm

app_name = 'customer'

urlpatterns = [
    path('', views.TransactionView.as_view(), name='index'),
    path('sign-in', auth_views.LoginView.as_view(
        template_name='signin.html', authentication_form=SignInForm), name='sign-in'),
    path('sign-up', views.SignUpView.as_view(), name='sign-up'),
    path('sign-out', auth_views.LogoutView.as_view(), name='sign-out'),
    path('<str:transaction_id>',
        login_required(views.AddAccountView.as_view()), name='add-account'),
]