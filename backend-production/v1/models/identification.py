#  Unisoft Group Copyright (c) 2023/1/26.
#
#  Created by Mahmudov Abdulloh
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan
import json

from django.db import models
from django_softdelete.models import SoftDeleteModel
from v1.models import Users


class Identification(SoftDeleteModel, models.Model):
    # code
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="identification")
    status = models.IntegerField('Status', default=0)
    code = models.CharField('Code', max_length=128, null=True)
    access_token = models.TextField('Access Token')
    expires_in = models.IntegerField('Expires In', default=0)
    token_type = models.CharField('Token Type', max_length=255)
    scope = models.CharField('Scope', max_length=255, null=True)
    refresh_token = models.TextField('Refresh Token', null=True)
    comparison_value = models.CharField('Comparison Value', max_length=255, null=True)
    seria = models.CharField('Seria', max_length=255, null=True)
    pinfl = models.CharField('Pinfl', max_length=255, null=True)
    response = models.JSONField('Response', null=True)
    image = models.TextField('Person Image', null=True)
    must_refresh_token = models.DateTimeField(auto_now_add=False, null=True, editable=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'user {str(self.user)} || status {self.status} || code {self.code}'
    def collection(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'response': json.loads(self.response),
            'created_at': self.created_at.strftime("%Y %d, %b %H:%M:%S"),
            'updated_at': self.updated_at.strftime("%Y %d, %b %H:%M:%S"),
        }

    class Meta:
        verbose_name_plural = "Identification"


class PreIdentification(SoftDeleteModel, models.Model):
    # code
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="pre_identification")
    firstname = models.CharField('firstname', max_length=255, null=True)
    lastname = models.CharField('lastname', max_length=255, null=True)
    seria = models.CharField('seria', max_length=255, null=True)
    birthday = models.CharField('birthday', max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def collection(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'seria': self.seria,
            'birthday': self.birthday,
            'created_at': self.created_at.strftime("%Y %d, %b %H:%M:%S"),
            'updated_at': self.updated_at.strftime("%Y %d, %b %H:%M:%S"),
        }

    class Meta:
        verbose_name_plural = "Identification"


class OneIDIdentification(SoftDeleteModel, models.Model):
    # code
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="one_id_identification")
    status = models.IntegerField('Status', default=0)
    access_token = models.TextField('Access Token')
    access_token_expires_in = models.IntegerField('Access Token Expires In', default=0)
    refresh_token = models.TextField('Refresh Token', null=True)
    refresh_token_expires_in = models.IntegerField('Refresh Token Expires In', default=0)
    must_refresh_token = models.DateTimeField(auto_now_add=False, null=True, editable=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
