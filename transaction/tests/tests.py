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