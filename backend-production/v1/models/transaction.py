from django.db import models
from django_softdelete.models import SoftDeleteModel
from .documents import Document_type, MFO, PurposeCode
from v1.models import ClientIABSAccount, Users
from v1.models.client import ClientInfo


class DocHistories(models.Model):
    client = models.ForeignKey(ClientInfo, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    tr_id = models.CharField(max_length=100, unique=True, db_index=True)
    ext_id = models.CharField(max_length=100, null=True)
    sender_company = models.CharField(max_length=512)
    sender_device = models.CharField(max_length=512)
    sender_company_account = models.CharField(max_length=255)
    sender_company_mfo = models.CharField(max_length=255)
    sender_company_inn = models.CharField(max_length=255)
    doc_type = models.CharField(max_length=256, null=True)
    transaction_date = models.DateField()
    number = models.CharField(max_length=255, null=True)
    personal_account = models.CharField(max_length=255, null=True)
    personal_inn = models.CharField(max_length=255, null=True)
    receiver_name = models.CharField(max_length=255, null=True)
    receiver_company_account = models.CharField(max_length=255)
    receiver_mfo = models.CharField(max_length=255, null=True)
    receiver_inn = models.CharField(max_length=255)
    receiver_purpose_code = models.CharField(max_length=255, null=True)
    contract_number = models.IntegerField(null=True)
    wiring_type = models.CharField(max_length=255, null=True)
    responsible = models.CharField(max_length=255, default='Мирсаидов Санжарбек Тимур угли')
    details = models.CharField(max_length=256, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True, default='Pending')
    credit_amount = models.FloatField(null=True)
    credit_description = models.CharField(max_length=255, null=True, blank=True)
    debit_amount = models.FloatField(null=True)
    debit_description = models.CharField(max_length=255, null=True, blank=True)
    draft_amount = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_credit = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.tr_id} || {self.ext_id}'

    def collection(self):
        return {
            "transaction_date": self.transaction_date.isoformat(),
            "credit_amount": self.credit_amount,
            "debit_amount": self.debit_amount,
            "receiver_mfo": self.receiver_mfo,
            "is_credit": self.is_credit,
        }

    class Meta:
        verbose_name = 'Document Histories'
        verbose_name_plural = 'Document Histories'


class Sample(SoftDeleteModel, models.Model):
    sender_account_name = models.ForeignKey(ClientIABSAccount, on_delete=models.DO_NOTHING,
                                            related_name='sender_sample')
    sender_mfo = models.ForeignKey(MFO, on_delete=models.DO_NOTHING, related_name='sender_mfo')
    doc_type = models.ForeignKey(Document_type, on_delete=models.DO_NOTHING, related_name='sender_doc_type_sample')
    sender_account = models.ForeignKey(ClientIABSAccount, on_delete=models.DO_NOTHING, related_name='sender_account')
    date = models.DateField()
    number = models.IntegerField()
    personal_account = models.CharField(max_length=100, null=True)
    inn_budget = models.CharField(max_length=30, null=True)
    details = models.CharField(max_length=256, null=True, blank=True)
    receiver_company = models.CharField(max_length=255, null=True, blank=True)
    receiver_account = models.ForeignKey(ClientIABSAccount, on_delete=models.DO_NOTHING,
                                         related_name='receiver_account')
    receiver_mfo = models.ForeignKey(MFO, on_delete=models.DO_NOTHING, related_name='receiver_mfo_sample')
    receiver_purpose_code = models.ForeignKey(PurposeCode, on_delete=models.DO_NOTHING)
    reciver_inn_pinfl = models.CharField(max_length=30, null=True)
    transfer_amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Document Sample'
        verbose_name_plural = 'Document Samples'


class DocTest(models.Model):
    client = models.ForeignKey(ClientInfo, on_delete=models.DO_NOTHING)
