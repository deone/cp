from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User

from rest_framework.test import APITestCase

from .data import *
from customer.models import Customer
from transaction.models import (
    Transaction, Inflow, Outflow)

from decimal import Decimal

class TestCustomer(TestCase):
    def setUp(self):
        super().setUp()

        # Create user
        user = User.objects.create_user(
            'mb@b.com', 'mb@b.com', 'password')

        # Create customer
        self.customer = Customer.objects.create(user=user, phone_number='0542224467')

    def tearDown(self):
        self.customer.delete()

class TestNGNToGHSTransaction(TestCase):
    def setUp(self):
        super().setUp()
        self.ngn_to_ghs_transaction = Transaction.objects.create(
            transaction_id='{}{}'.format('SMNY', timezone.now().strftime('%y%m%d%H%M%S')))

        # Create inflow
        source_amount = Decimal('10000')
        source_currency = 'NGN'

        Inflow.objects.create(
            transaction=self.ngn_to_ghs_transaction,
            currency=source_currency,
            amount=source_amount,
        )

        # Create outflow
        dest_amount = Decimal('123.45')
        dest_currency = 'GHS'

        Outflow.objects.create(
            transaction=self.ngn_to_ghs_transaction,
            currency=dest_currency,
            amount=dest_amount,
        )

    def tearDown(self):
        self.ngn_to_ghs_transaction.delete()

class UpdatedTestNGNToGHSTransaction(TestNGNToGHSTransaction, TestCustomer):
    def setUp(self):
        super().setUp()
        # Update transaction
        self.transaction_id = '{}{}'.format(
            'SMNY', timezone.now().strftime('%y%m%d%H%M%S'))
        self.ngn_to_ghs_transaction.user = self.customer.user
        self.ngn_to_ghs_transaction.transaction_id = self.transaction_id
        self.ngn_to_ghs_transaction.save()

        # Update outflow
        self.ngn_to_ghs_transaction.outflow.dest_account_provider_code = 'mtn'
        self.ngn_to_ghs_transaction.outflow.dest_account_number = '0546789100'
        self.ngn_to_ghs_transaction.outflow.save()

class SaveNairaPaymentInfoTest(APITestCase, UpdatedTestNGNToGHSTransaction):
    def setUp(self):
        super().setUp()
        self.ngn_to_ghs_transaction.user = self.customer.user
        self.ngn_to_ghs_transaction.transaction_id = 'CSHP201208155232267518'
        self.ngn_to_ghs_transaction.save()

    def test_GET_cancelled(self):
        url = '{}{}{}'.format(
            '/t/save-naira-payment-info?txref=',
            self.ngn_to_ghs_transaction.transaction_id, '&cancelled=true')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)        
        self.assertEqual(response.url, '/')

        self.ngn_to_ghs_transaction.refresh_from_db()
        self.assertEqual(self.ngn_to_ghs_transaction.status, 'Cancelled')

    def test_POST(self):
        url = '{}{}{}'.format('/t/save-naira-payment-info?txref=',
            self.ngn_to_ghs_transaction.transaction_id, '&flwref=FLW200801778')
        data = naira_payment_info(self.ngn_to_ghs_transaction.transaction_id)

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

        self.ngn_to_ghs_transaction.refresh_from_db()
        self.assertTrue(self.ngn_to_ghs_transaction.inflow.reference)