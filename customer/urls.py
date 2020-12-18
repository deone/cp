from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from . import views
from .forms import SignInForm

app_name = 'customer'

urlpatterns = [
    path('', views.TransactionView.as_view(), name='index'),
    path('get-accounts', login_required(views.GetAccountsView.as_view())),
    path('activity', login_required(views.TransactionListView.as_view())),
    path('sign-in', auth_views.LoginView.as_view(
        template_name='signin.html', authentication_form=SignInForm), name='sign-in'),
    path('sign-up', views.SignUpView.as_view(), name='sign-up'),
    path('sign-out', auth_views.LogoutView.as_view(), name='sign-out'),
    path('<str:transaction_id>',
        login_required(views.AddAccountView.as_view()), name='add-account'),
    path('<str:transaction_id>/confirm',
        login_required(views.ConfirmTransactionView.as_view()), name='confirm-transaction'),
]