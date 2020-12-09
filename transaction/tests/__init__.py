from django.test import TestCase
from django.utils import timezone

from customer.tests import TestCustomer
from transaction.models import (Transaction, Inflow, Outflow)

from decimal import Decimal

class TestNGNToGHSTransaction(TestCase):
    def setUp(self):
        super().setUp()
        self.ngn_to_ghs_transaction = Transaction.objects.create(transaction_id='CSHP201208155232267518')

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

class TestGHSToNGNTransaction(TestCase):
    def setUp(self):
        super().setUp()
        self.ghs_to_ngn_transaction = Transaction.objects.create(transaction_id='CSHP201208155232267519')

        # Create inflow
        source_currency = 'GHS'
        source_amount = Decimal('100')

        Inflow.objects.create(
            transaction=self.ghs_to_ngn_transaction,
            currency=source_currency,
            amount=source_amount,
        )

        # Create outflow
        dest_amount = Decimal('7813')
        dest_currency = 'GHS'

        Outflow.objects.create(
            transaction=self.ghs_to_ngn_transaction,
            currency=dest_currency,
            amount=dest_amount,
        )

    def tearDown(self):
        self.ghs_to_ngn_transaction.delete()

class UpdatedTestGHSToNGNTransaction(TestGHSToNGNTransaction, TestCustomer):
    def setUp(self):
        super().setUp()
        # Update transaction
        self.transaction_id = '{}{}'.format(
            'SMNY', timezone.now().strftime('%y%m%d%H%M%S'))
        self.ghs_to_ngn_transaction.user = self.customer.user
        self.ghs_to_ngn_transaction.transaction_id = self.transaction_id
        self.ghs_to_ngn_transaction.save()

        # Update outflow
        self.ghs_to_ngn_transaction.outflow.dest_account_provider_code = '044'
        self.ghs_to_ngn_transaction.outflow.dest_account_number = '0690000032'
        self.ghs_to_ngn_transaction.outflow.save()