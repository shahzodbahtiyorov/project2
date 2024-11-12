#  Unisoft Group Copyright (c) 2023/1/26.
#
#  Created by Mahmudov Abdulloh
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan

from django.db import models

from api import settings
import datetime


class Error(models.Model):
    # code
    code = models.IntegerField('Error code')
    alias = models.IntegerField('Alias Code from origin', null=True)
    origin = models.CharField('Origin', max_length=50, default=settings.APP_NAME)
    en = models.CharField("English", max_length=255)
    uz = models.CharField("O'zbekcha", max_length=255, null=True)
    ru = models.CharField("Русский", max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "6. Errors"

    pass


class Service(models.Model):
    method = models.CharField("Method Name", max_length=60)
    is_active = models.BooleanField(default=True)
    is_test = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "7. Services"


class RequestModel(models.Model):
    method = models.CharField(max_length=50)
    user = models.CharField(max_length=255)
    count = models.BigIntegerField(default=1)
    date_created = models.DateField(default=datetime.datetime.now)

    def str(self):
        return f"{self.method} - {self.user}"

    def increment(self):
        self.count += 1
        self.save()
