from rest_framework.test import APITestCase

from .data import *
from . import (
    UpdatedTestNGNToGHSTransaction,
    UpdatedTestGHSToNGNTransaction,
    UpdatedTestBTCToNGNTransaction
)

class SaveNairaPaymentInfoTest(APITestCase, UpdatedTestNGNToGHSTransaction):
    def test_GET_cancelled(self):
        url = '{}{}{}'.format(
            '/t/save-naira-payment-info?txref=',
            self.transaction.transaction_id, '&cancelled=true')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)        
        self.assertEqual(response.url, '/activity')

        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.status, 'Cancelled')

    def test_POST(self):
        url = '{}{}{}'.format('/t/save-naira-payment-info?txref=',
            self.transaction.transaction_id, '&flwref=FLW200801778')
        data = naira_payment_info(self.transaction.transaction_id)

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/activity')

        self.transaction.refresh_from_db()
        self.assertTrue(self.transaction.inflow.reference)

class HandleNairaPaymentUpdateTest(APITestCase, UpdatedTestNGNToGHSTransaction):
    def setUp(self):
        super().setUp()
        self.url = '/t/handle-naira-update'
        self.data = naira_payment_update_card(self.transaction.transaction_id)

    def test_POST(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, 200)

        # Check that inflow is updated
        inflow = self.transaction.inflow
        inflow.refresh_from_db()
        self.assertEqual(inflow.source_account_provider, 'card')
        self.assertEqual(inflow.source_account_number, '539983******9335')
        self.assertTrue(inflow.is_complete)
        self.assertTrue(inflow.updated_at)

class HandleCediTransferUpdate(APITestCase, UpdatedTestNGNToGHSTransaction):
    def setUp(self):
        super().setUp()
        self.url = '/t/handle-cedi-transfer-update'

    def test_POST(self):
        data = cedi_transfer_update(self.transaction.transaction_id)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 200)

        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.outflow.reference, data['transaction_id'])
        self.assertTrue(self.transaction.outflow.is_complete)
        self.assertTrue(self.transaction.is_complete)
        self.assertEqual(self.transaction.status, 'Successful')

class SaveCediPaymentInfoTest(APITestCase, UpdatedTestGHSToNGNTransaction):
    def test_GET(self):
        url = '{}{}'.format('/t/save-cedi-payment-info?',
            cedi_payment_info(self.transaction.transaction_id))

        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/activity')

        self.transaction.refresh_from_db()
        self.assertTrue(self.transaction.inflow.reference)
        self.assertTrue(self.transaction.inflow.source_account_number)
        self.assertTrue(self.transaction.inflow.source_account_provider)

class HandleCediPaymentUpdateTest(APITestCase, UpdatedTestGHSToNGNTransaction):
    def setUp(self):
        super().setUp()
        self.url = '/t/handle-cedi-payment-update'
        self.data = cedi_payment_update(self.transaction.transaction_id)

    def test_POST(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, 200)

        # Check that inflow and outflow are updated
        self.transaction.inflow.refresh_from_db()
        self.assertTrue(self.transaction.inflow.is_complete)
        self.assertTrue(self.transaction.inflow.updated_at)

        self.transaction.outflow.refresh_from_db()
        self.assertTrue(self.transaction.outflow.reference)

class HandleNairaTransferUpdate(APITestCase, UpdatedTestGHSToNGNTransaction):
    def setUp(self):
        super().setUp()
        self.url = '/t/handle-naira-update'
        self.data = naira_transfer_update(self.transaction.transaction_id)

    def test_POST(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, 200)

        self.transaction.refresh_from_db()
        self.assertTrue(self.transaction.outflow.is_complete)
        self.assertTrue(self.transaction.is_complete)
        self.assertEqual(self.transaction.status, 'Successful')

class HandleBTCPaymentUpdateTest(APITestCase, UpdatedTestBTCToNGNTransaction):
    def setUp(self):
        super().setUp()
        self.url = '/t/handle-btc-payment-update'
        self.data = btc_payment_update(
            self.transaction.transaction_id, self.transaction.user.id)

    def test_POST(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 200)

        # Check that inflow and outflow are updated
        inflow = self.transaction.inflow
        inflow.refresh_from_db()
        self.assertEqual(inflow.reference, self.data['id'])
        self.assertTrue(self.transaction.inflow.is_complete)
        self.assertTrue(self.transaction.inflow.updated_at)

        self.transaction.outflow.refresh_from_db()
        self.assertTrue(self.transaction.outflow.reference)