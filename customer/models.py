from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)

class RecipientAccount(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    _type = models.CharField(max_length=6)
    name = models.CharField(max_length=50, null=True, blank=True) # this can be null since we can't get wallet names for now
    number = models.CharField(max_length=10)
    confirm_number = models.CharField(max_length=10, null=True)
    provider_code = models.CharField(max_length=15)
    provider_name = models.CharField(max_length=50)