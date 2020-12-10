from rest_framework.test import APITestCase

from .data import *
from . import UpdatedTestNGNToGHSTransaction, UpdatedTestGHSToNGNTransaction

class SaveNairaPaymentInfoTest(APITestCase, UpdatedTestNGNToGHSTransaction):
    def test_GET_cancelled(self):
        url = '{}{}{}'.format(
            '/t/save-naira-payment-info?txref=',
            self.transaction.transaction_id, '&cancelled=true')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)        
        self.assertEqual(response.url, '/')

        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.status, 'Cancelled')

    def test_POST(self):
        url = '{}{}{}'.format('/t/save-naira-payment-info?txref=',
            self.transaction.transaction_id, '&flwref=FLW200801778')
        data = naira_payment_info(self.transaction.transaction_id)

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

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
        self.assertEqual(response.url, '/')

        self.transaction.refresh_from_db()
        self.assertTrue(self.transaction.inflow.reference)
        self.assertTrue(self.transaction.inflow.source_account_number)
        self.assertTrue(self.transaction.inflow.source_account_provider)

class HandleCediPaymentUpdateTest(APITestCase, UpdatedTestGHSToNGNTransaction):
    def setUp(self):
        super().setUp()
        self.url = '/t/handle-cedi-payment-update'
        self.data = cedi_payment_update(self.transaction.transaction_id)
        print(self.transaction)
        print(self.transaction.outflow)

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

""" class HandleBTCPaymentUpdate(APITestCase, UpdatedTestBTCToNGNTransaction):
    def setUp(self):
        super().setUp()
        # Create transactions
        ngn_data = copy.deepcopy(self.ngn_transaction_data)
        ngn_data.update({
            # let's use a random id so we can
            # get valid response from Rave
            # every time.
            'id': random.randint(1, 10000),
            'user': self.user,
            'dest_account': self.bank_account,
            'invoice_created_at': timezone.now()
        })
        ghs_data = copy.deepcopy(self.ghs_transaction_data)
        ghs_data.update({
            # let's use a random id so we can
            # get valid response from Rave
            # every time.
            'id': random.randint(1, 10000),
            'user': self.user,
            'dest_account': self.wallet,
            'invoice_created_at': timezone.now()
        })
        self.ngn_transaction = Transaction.objects.create(**ngn_data)
        self.ghs_transaction = Transaction.objects.create(**ghs_data)

    def _get_data(self, pk, url):
        return {
            'id': '0f0008fb-9aca-452c-a355-74b1c526dda3',
            'callback_url': '{}{}'.format('http://185.20.49.94:25155', url),
            'success_url': 'http://185.20.49.94:25155/activity',
            'status': 'paid',
            'order_id': pk,
            'user_id': self.user.pk,
            'description': 'BTC to NGN',
            'price': '100000',
            'fee': '0',
            'auto_settle': '0',
            'hashed_order': '3d1ee193b12bf9b3343e69b31dccc8787c0278cc4e8897f021640a5e9d12fe40'
        }

    def test_update_source_invoice_paid_ngn_transaction(self):
        url = '{}{}{}'.format('/t/', self.ngn_transaction.pk, '/update-source')
        data = self._get_data(self.ngn_transaction.pk, url)

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"message":"Success"}')

        t = Transaction.objects.get(pk=self.ngn_transaction.pk)
        self.assertTrue(t.source_debited_at is not None)
        self.assertEqual(t.source_transaction_id, data['id'])
        self.assertTrue(t.transfer_initiated_at is not None)

    def test_update_source_invoice_paid_ghs_transaction(self):
        url = '{}{}{}'.format('/t/', self.ghs_transaction.pk, '/update-source')
        data = self._get_data(self.ghs_transaction.pk, url)

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"message":"Success"}')

        t = Transaction.objects.get(pk=self.ghs_transaction.pk)
        self.assertTrue(t.source_debited_at is not None)
        self.assertEqual(t.source_transaction_id, data['id'])
        self.assertTrue(t.transfer_initiated_at is not None)

    def tearDown(self):
        self.ngn_transaction.delete()
        self.ghs_transaction.delete() """