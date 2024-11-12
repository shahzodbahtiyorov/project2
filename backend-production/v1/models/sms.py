#  Unisoft Group Copyright (c) 2023/1/26.
#
#  Created by Mahmudov Abdulloh
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan

from django.db import models


class Sms(models.Model):
    mobile = models.CharField('Phone Number', max_length=64)
    otp_token = models.CharField('Otp token', max_length=255, null=True)
    additional = models.CharField('Additional', max_length=255, null=True)
    tr_id = models.CharField('Transaction ID', max_length=255, null=True)
    lang = models.CharField('Language', max_length=255, null=True)
    expire = models.BooleanField('Expire', default=False)
    tried = models.IntegerField('Tried')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "✉️Sms"
