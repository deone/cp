from rest_framework.test import APITestCase

from .data import *
from . import UpdatedTestNGNToGHSTransaction

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

class HandleNairaPaymentUpdateTest(APITestCase, UpdatedTestNGNToGHSTransaction):
    def setUp(self):
        super().setUp()
        self.url = '/t/handle-naira-update'
        self.data = naira_payment_update_card(self.ngn_to_ghs_transaction.transaction_id)

    def test_POST(self):
        transaction = self.ngn_to_ghs_transaction
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, 200)

        # Check that inflow is updated
        inflow = transaction.inflow
        inflow.refresh_from_db()
        self.assertEqual(inflow.source_account_provider, 'card')
        self.assertEqual(inflow.source_account_number, '539983******9335')
        self.assertTrue(inflow.is_complete)
        self.assertTrue(inflow.updated_at)

class HandleCediTransferUpdate(APITestCase, UpdatedTestNGNToGHSTransaction):
    def setUp(self):
        super().setUp()
        self.url = '/t/handle-cedi-transfer-update'
        self.transaction = self.ngn_to_ghs_transaction

    def test_POST(self):
        data = cedi_transfer_update(self.transaction.transaction_id)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 200)

        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.outflow.reference, data['transaction_id'])
        self.assertTrue(self.transaction.outflow.is_complete)
        self.assertTrue(self.transaction.is_complete)
        self.assertEqual(self.transaction.status, 'Successful')