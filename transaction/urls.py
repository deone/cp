from django.urls import path

from . import views

app_name = 'transaction'
urlpatterns = [
    path('save-naira-payment-info',
        views.save_naira_payment_info, name='save-naira-payment-info'),
    path('save-cedi-payment-info',
        views.save_cedi_payment_info, name='save-cedi-payment-info'),
    path('handle-cedi-payment-update',
        views.handle_cedi_payment_update, name='handle-cedi-payment-update'),
    path('handle-naira-update',
        views.handle_naira_update, name='handle-naira-update'),
    path('handle-cedi-transfer-update',
        views.handle_cedi_transfer_update, name='handle-cedi-transfer-update'),
]