from django.test import TestCase
from django.contrib.auth.models import User

from customer.models import Customer

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