from django.db import models
from django_softdelete.models import SoftDeleteModel
from v1.models.client import ClientInfo


class Report(SoftDeleteModel, models.Model):
    expense_article = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(ClientInfo, related_name='reports', on_delete=models.CASCADE)

    def __str__(self):
        return self.expense_article


class ClientIABSAccount(SoftDeleteModel, models.Model):
    client = models.ForeignKey(ClientInfo, on_delete=models.DO_NOTHING)
    number = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    is_primary = models.BooleanField(default=False)
    inn = models.CharField(max_length=20)
    mfo = models.CharField(max_length=20)
    iabs_id = models.CharField(max_length=255)
    balance = models.FloatField(max_length=255)
    currency_code = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_document = models.BooleanField(default=False)
    is_report = models.BooleanField(default=False)
    codeCoa = models.CharField(max_length=255)
    created_accaunt_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.iabs_id} -- {self.name} || Active: {self.is_active} || Primary: {self.is_primary}'
