from django.test import TestCase
from django.utils import timezone

from customer.tests import TestCustomer
from transaction.models import (Transaction, Inflow, Outflow)

from decimal import Decimal

class TestNGNToGHSTransaction(TestCase):
    def setUp(self):
        super().setUp()
        self.transaction = Transaction.objects.create(
            transaction_id='{}{}'.format('TMNY', timezone.now().strftime('%y%m%d%H%M%S%f')))

        # Create inflow
        Inflow.objects.create(
            transaction=self.transaction,
            currency='NGN',
            amount=Decimal('10000'),
        )

        # Create outflow
        Outflow.objects.create(
            transaction=self.transaction,
            currency='GHS',
            amount=Decimal('123.45'),
        )

    def tearDown(self):
        self.transaction.delete()

class UpdatedTestNGNToGHSTransaction(TestNGNToGHSTransaction, TestCustomer):
    def setUp(self):
        super().setUp()
        # Update transaction
        self.transaction.user = self.customer.user
        self.transaction.save()

        # Update outflow
        self.transaction.outflow.dest_account_provider_code = 'mtn'
        self.transaction.outflow.dest_account_number = '0546789100'
        self.transaction.outflow.save()

class TestGHSToNGNTransaction(TestCase):
    def setUp(self):
        super().setUp()
        self.transaction = Transaction.objects.create(
            transaction_id='{}{}'.format('TMNY', timezone.now().strftime('%y%m%d%H%M%S%f')))

        # Create inflow
        Inflow.objects.create(
            transaction=self.transaction,
            currency='GHS',
            amount=Decimal('100'),
        )

        # Create outflow
        Outflow.objects.create(
            transaction=self.transaction,
            currency='GHS',
            amount=Decimal('7813'),
        )

    def tearDown(self):
        self.transaction.delete()

class UpdatedTestGHSToNGNTransaction(TestGHSToNGNTransaction, TestCustomer):
    def setUp(self):
        super().setUp()
        # Update transaction
        self.transaction.user = self.customer.user
        self.transaction.save()

        # Update outflow
        self.transaction.outflow.dest_account_provider_code = '044'
        self.transaction.outflow.dest_account_number = '0690000032'
        self.transaction.outflow.save()

""" class TestBTCToNGNTransaction(TestCase):
    def setUp(self):
        super().setUp()
        self.transaction = Transaction.objects.create(transaction_id='CSHP201208155232267520')

        # Create inflow
        Inflow.objects.create(
            transaction=self.btc_to_ngn_transaction,
            currency='BTC',
            amount=Decimal('0.0001'),
        )

        # Create outflow
        Outflow.objects.create(
            transaction=self.btc_to_ngn_transaction,
            currency='NGN',
            amount=Decimal('734.133'),
        )

    def tearDown(self):
        self.transaction.delete()

class UpdatedTestBTCToNGNTransaction(TestBTCToNGNTransaction, TestCustomer):
    def setUp(self):
        super().setUp()
        # Update transaction
        self.transaction.user = self.customer.user
        self.transaction.save()

        # Update outflow
        self.transaction.outflow.dest_account_provider_code = '044'
        self.transaction.outflow.dest_account_number = '0690000035'
        self.transaction.outflow.save() """