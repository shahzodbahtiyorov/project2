#  Unisoft Group Copyright (c) 2023/1/26.
#
#  Created by Mahmudov Abdulloh
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan

from django.db import models
from django_softdelete.models import SoftDeleteModel

from v1.models import Users


# a1.delete()  # soft deletion of object
# deleted_a1.restore()  # restores deleted object
# Article.deleted_objects.count()
# a1.hard_delete()  # deletes the object at all.

class Card(SoftDeleteModel, models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="cards")
    name = models.CharField(max_length=128)
    balance = models.FloatField(max_length=128)
    number = models.CharField(max_length=255, default=0)
    expire = models.CharField(max_length=255, null=True)
    mask = models.CharField(max_length=128)
    token = models.CharField(max_length=128, null=True, db_index=True)
    card_owner = models.CharField(max_length=256, null=True)
    card_logo = models.CharField(max_length=128)
    bank_logo = models.CharField(max_length=128, null=True, blank=True)
    is_unired = models.IntegerField()
    is_alias = models.BooleanField(default=False)
    is_primary = models.IntegerField()
    is_verified = models.IntegerField(default=0)
    card_registered_phone = models.CharField(max_length=50, null=True)
    is_salary = models.IntegerField()
    type = models.IntegerField()  # ?!  0-UZCARD  1-HUMO  2-VISA  3-TCB
    to_balance_sum = models.BooleanField(default=True)
    blocked = models.IntegerField(default=0)  # ?
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    # created_at = models.DateTimeField(auto_now_add=False, null=True, editable=True)
    # updated_at = models.DateTimeField(auto_now_add=False, null=True, editable=True)

    class Meta:
        verbose_name_plural = "💳Cards"

    def collection(self):
        return {
            'id': self.id,
            'user': self.user_id,
            'name': self.name,
            'balance': self.balance / 100,
            'mask': self.mask,
            'number': self.number,
            'token': self.token,
            'expire_date': '0000',
            'card_owner': self.card_owner,
            'card_logo': self.card_logo,
            'bank_logo': self.bank_logo,
            'is_unired': self.is_unired,
            'is_primary': self.is_primary,
            'is_verified': self.is_verified,
            'card_registered_phone': self.card_registered_phone,
            'is_salary': self.is_salary,
            'type': self.type,
            'blocked': self.blocked,
            'created_at': self.created_at.strftime("%d %b, %Y"),
            'updated_at': self.updated_at.strftime("%d %b, %Y"),
        }


class Form(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="form")
    ext_id = models.CharField(max_length=128)
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name_plural = "Form"


class CardHistoryModel(models.Model):
    card_id = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="history")
    amount = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField()
    terminal = models.CharField(max_length=255, null=True, blank=True)
    merchant = models.CharField(max_length=255, null=True, blank=True)
    merchant_name = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    credit = models.BooleanField(null=True)
    reversal = models.BooleanField(null=True, blank=True)

    class Meta:
        ordering = ["created_at"]

    def collection(self):
        return {
            "card_number": self.card_id.number,
            "amount": self.amount,
            "created_at": self.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
            "terminal": self.terminal,
            "merchant": self.merchant,
            "merchant_name": self.merchant_name,
            "city": self.city,
            "credit": self.credit,
            "reversal": self.reversal,

        }
