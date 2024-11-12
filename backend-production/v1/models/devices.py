#  Unisoft Group Copyright (c) 2023/1/26.
#
#  Created by Mahmudov Abdulloh
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan
from apscheduler.schedulers.background import BackgroundScheduler
from django.db import models

from v1.models import Users


class Device(models.Model):
    # code
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="device")
    ip = models.CharField('Device ip', max_length=30, null=True)
    imei = models.CharField('Device imei', max_length=100, null=True)
    mac = models.CharField('Device mac', max_length=100, null=True)
    core_id = models.CharField('Device core id', max_length=100)
    name = models.CharField('Device name', max_length=100, null=True)
    firebase_reg_id = models.CharField('Device firebase_reg_id', max_length=255, null=True)
    uuid = models.CharField('Device uuid', max_length=100)
    verified = models.BooleanField('Device verified', default=False)
    tries = models.IntegerField('Device tries', default=0)
    is_blocked = models.BooleanField('Device blocked', default=False)
    version = models.CharField('Device version', max_length=20, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "10. Device"

    def __str__(self):
        return f'{self.name} -- "{self.user.username}"'

    def save(self, *args, **kwargs):
        if self.tries >= 3:
            self.is_blocked = True
        super().save(*args, **kwargs)


class SingletonScheduler:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = BackgroundScheduler()
        return cls._instance
