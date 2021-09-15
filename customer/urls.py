from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from . import views
from .forms import SignInForm, TPasswordResetForm, TSetPasswordForm

app_name = 'customer'

urlpatterns = [
    path('', views.TransactionView.as_view(), name='index'),
    path('get-accounts', login_required(views.GetAccountsView.as_view())),
    path('activity', login_required(views.TransactionListView.as_view()), name='activity'),
    path('sign-in', auth_views.LoginView.as_view(
        template_name='signin.html', authentication_form=SignInForm), name='sign-in'),
    path('sign-up', views.SignUpView.as_view(), name='sign-up'),
    path('sign-out', auth_views.LogoutView.as_view(), name='sign-out'),
    path('<int:pk>',
        login_required(views.TransactionDetailView.as_view()), name='transaction-detail'),
    path('<str:transaction_id>/add-account',
        login_required(views.AddAccountView.as_view()), name='add-account'),
    path('<str:transaction_id>/confirm',
        login_required(views.ConfirmTransactionView.as_view()), name='confirm-transaction'),
    path('password-reset', auth_views.PasswordResetView.as_view(
        template_name='customer/password_reset_form.html',
        email_template_name='customer/password_reset_email.html',
        subject_template_name='customer/password_reset_subject.txt',
        form_class=TPasswordResetForm,
        from_email='noreply@transfr.money',
        success_url='/password-reset-done',
    ), name='password-reset'),
    path('password-reset-done', auth_views.PasswordResetDoneView.as_view(
        template_name='customer/password_reset_done.html'
    ), name='password-reset-done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name='customer/password_reset_confirm.html',
        form_class=TSetPasswordForm,
        success_url='/password-reset-complete',
    ), name='password-reset-confirm'),
    path('password-reset-complete', auth_views.PasswordResetCompleteView.as_view(
        template_name='customer/password_reset_complete.html'
    ), name='password-reset-complete'),
]