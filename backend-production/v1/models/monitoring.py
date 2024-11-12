#  Unisoft Group Copyright (c) 2023/1/26.
#
#  Created by Mahmudov Abdulloh
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan
import datetime
import json
import uuid

import jsonfield
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from v1.helper import helper, transfer_type_description, transfer_type, transfer_pay_type, transfer_description
from django_softdelete.models import SoftDeleteModel

from v1.models import Users, Card


class Monitoring(SoftDeleteModel):
    # code
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="monitoring")
    tr_id = models.CharField(max_length=255, null=True, unique=True, db_index=True)
    t_id = models.CharField(max_length=255, null=True)
    type = models.IntegerField(null=True)
    pay_type = models.IntegerField(null=True)
    sender_token = models.CharField(max_length=255, null=True)
    sender_number = models.CharField(max_length=100, null=True)
    sender_expire = models.CharField(max_length=10, null=True)
    sender_mask = models.CharField(max_length=100, null=True)
    sender_name = models.CharField(max_length=255, null=True)
    receiver_token = models.CharField(max_length=255, null=True)
    receiver_number = models.CharField(max_length=100, null=True)
    receiver_mask = models.CharField(max_length=100, null=True)
    receiver_name = models.CharField(max_length=255, null=True)
    receiver = models.CharField(max_length=255, null=True)
    debit_state = models.CharField(max_length=64, null=True)
    debit_description = models.CharField(max_length=255, null=True)
    debit_amount = models.FloatField(null=True)
    debit_currency = models.CharField(max_length=10, null=True)
    credit_state = models.CharField(max_length=64, null=True)
    credit_description = models.CharField(max_length=255, null=True)
    credit_amount = models.FloatField(null=True)
    credit_currency = models.CharField(max_length=10, null=True)
    # home = models.ForeignKey(HomeModel, on_delete=models.SET_NULL, null=True, blank=True)
    rate = models.FloatField(null=True)
    commission = models.FloatField(null=True)
    description = jsonfield.JSONField(null=True)
    type_description = jsonfield.JSONField(null=True)
    merchant = models.CharField(max_length=64, null=True)
    terminal = models.CharField(max_length=64, null=True)
    note = models.CharField(max_length=512, null=True)
    is_credit = models.IntegerField(default=1)
    is_saved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    # created_at = models.DateTimeField(auto_now_add=False, null=True, editable=True)
    # updated_at = models.DateTimeField(auto_now_add=False, null=True, editable=True)

    def row_save(self, user, sender, receiver_data, t_type, pay_type, com_type, amount, currency, note):
        receiver_name = receiver_data['name']
        # data = {
        #     'number': receiver_data['number']
        # }
        # result = mts_gateway.post('api/v1/main/', 'get.receiver.owner', data)
        # if 'result' in result:
        #     receiver_name = result['result']['owner']
        expire = sender['expire']
        if com_type == 'uzcard_to_visa_sum' or com_type == 'humo_to_visa_sum' or com_type == 'visa_sum_to_uzcard' or \
                com_type == 'visa_sum_to_humo' or com_type == 'visa_sum_to_visa_sum':
            expire = expire
        commission = Commission.objects.filter(name=com_type).first()
        com = (commission.percentage * amount) / 100
        is_credit = 1
        if receiver_data['token']:
            is_credit = 2
        self.user = user
        self.tr_id = 'U_M_T_' + f"{uuid.uuid4()}"
        self.t_id = 'U_M_T_' + f"{uuid.uuid4()}"
        self.type = t_type
        self.pay_type = pay_type
        self.sender_token = sender['token']
        self.sender_number = sender['number']
        self.sender_expire = expire
        self.sender_mask = sender['mask']
        self.sender_name = sender['name']
        self.receiver_token = receiver_data['token']
        self.receiver_number = receiver_data['number']
        self.receiver_mask = helper.card_mask(receiver_data['number'])
        self.receiver = receiver_data['number']
        self.receiver_name = receiver_name
        self.debit_state = transfer_description.CREATED
        self.debit_description = 'Created'
        self.debit_amount = amount
        self.debit_currency = currency
        self.credit_state = transfer_description.CREATED
        self.credit_description = 'Created'
        self.credit_amount = amount
        self.credit_currency = currency
        self.rate = 0
        self.commission = com
        self.description = transfer_description.get_description(transfer_description.CREATED)
        self.type_description = transfer_type_description.get_description(transfer_type.TRANSFER)
        self.merchant = commission.in_merchant
        self.terminal = commission.in_terminal
        self.note = note
        self.is_credit = is_credit
        self.save()

    def collection(self):
        is_credit = False
        if self.is_credit == 2:
            is_credit = True
        sender_name = self.sender_name
        if not self.sender_name:
            card = Card.objects.filter(token=self.sender_token).first()
            if card:
                monitoring = Monitoring.objects.filter(id=self.id).first()
                monitoring.sender_name = card.card_owner
                monitoring.save()
                sender_name = card.card_owner

        json_string = self.description

        # Parsing the JSON string into a Python dictionary
        if isinstance(json_string, str):
            json_data = json.loads(json_string)
            self.description = json_data
            self.save()
        else:
            json_data = json_string

        json_string1 = self.type_description

        # Parsing the JSON string into a Python dictionary
        if isinstance(json_string1, str):
            json_data1 = json.loads(json_string1)
            self.type_description = json_data1
            self.save()
        else:
            json_data1 = json_string1
        return {
            'is_local': True,
            'is_credit': is_credit,
            'tr_id': self.tr_id,
            'type': self.type,
            'pay_type': self.pay_type,
            'sender': {
                'token': self.sender_token,
                'number': self.sender_number,
                'expire': '0000',
                'mask': self.sender_mask,
                'name': sender_name,
            },
            'receiver': {
                'token': self.receiver_token,
                'number': self.receiver_number,
                'mask': self.receiver_mask,
                'receiver': self.receiver,
                'name': self.receiver_name,
            },
            'debit': {
                'state': self.debit_state,
                'description': self.debit_description,
                'amount': self.debit_amount,
                'currency': self.debit_currency,
            },
            'credit': {
                'state': self.credit_state,
                'description': self.credit_description,
                'amount': self.credit_amount,
                'currency': self.credit_currency,
            },
            'rate': self.rate,
            'commission': self.commission,
            'description': json_data,
            'type_description': json_data1,
            'merchant': self.merchant,
            'terminal': self.terminal,
            # 'created_at': self.created_at.strftime("%d.%m.%Y %H:%M:%S"),
            # 'updated_at': self.updated_at.strftime("%d.%m.%Y %H:%M:%S"),
            'created_at': (self.created_at + datetime.timedelta(hours=5)).strftime("%d.%m.%Y %H:%M:%S"),
            'updated_at': (self.updated_at + datetime.timedelta(hours=5)).strftime("%d.%m.%Y %H:%M:%S"),
        }

    def home_collection(self):
        return {
            'id': self.id,
            'sender': self.sender_mask,
            'receiver': self.receiver_number,
            'receiver_name': self.receiver_name,
            'amount': self.credit_amount,
            'currency': int(self.credit_currency),
            'type': self.type,
            'pay_type': self.pay_type,
            'created_at': (self.created_at + datetime.timedelta(hours=5)).strftime("%d.%m.%Y %H:%M:%S"),
            'updated_at': (self.updated_at + datetime.timedelta(hours=5)).strftime("%d.%m.%Y %H:%M:%S"),
        }

    class Meta:
        verbose_name_plural = "📈Monitoring"
        ordering = ["-created_at"]


class Commission(models.Model):
    name = models.CharField(max_length=128, null=True)
    in_merchant = models.CharField(max_length=64, null=True)
    in_terminal = models.CharField(max_length=64, null=True)
    in_terminal_account = models.CharField(max_length=128, null=True)
    out_merchant = models.CharField(max_length=64, null=True)
    out_terminal = models.CharField(max_length=64, null=True)
    out_terminal_account = models.CharField(max_length=128, null=True)
    percentage = models.FloatField(max_length=10, null=True, default=0.0)

    def collection(self):
        return {
            'name': self.name,
            'percentage': self.percentage,
        }


class TransferSave(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="transfer_save")
    sender = models.CharField(max_length=64, null=True)
    receiver = models.CharField(max_length=64, null=True)
    amount = models.FloatField(null=True)
    currency = models.IntegerField(null=True)
    type = models.IntegerField(null=True)
    pay_type = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def collection(self):
        return {
            'id': self.id,
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount,
            'currency': self.currency,
            'type': self.type,
            'pay_type': self.pay_type,
            'created_at': self.created_at.strftime("%Y %d, %b %H:%M:%S"),
            'updated_at': self.updated_at.strftime("%Y %d, %b %H:%M:%S")
        }


class PaynetSave(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="paynet_save")
    category_id = models.IntegerField(null=True)
    provider_id = models.IntegerField(null=True)
    service_id = models.IntegerField(null=True)
    fields = models.JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def collection(self):
        return {
            'id': self.id,
            'category_id': self.category_id,
            'provider_id': self.provider_id,
            'service_id': self.service_id,
            'fields': self.fields,
            'created_at': self.created_at.strftime("%Y %d, %b %H:%M:%S"),
            'updated_at': self.updated_at.strftime("%Y %d, %b %H:%M:%S")
        }


@receiver(pre_save, sender=Monitoring)
def null_created_at(sender, instance: Monitoring = None, created=None, **kwargs):
    if not instance.created_at:
        instance.created_at = datetime.datetime.now() + datetime.timedelta(hours=5)
    if not instance.updated_at:
        instance.updated_at = datetime.datetime.now() + datetime.timedelta(hours=5)
