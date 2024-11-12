from django.db import models

from django_softdelete.models import SoftDeleteModel


class PurposeCode(SoftDeleteModel, models.Model):
    code = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.code


class MFO(SoftDeleteModel, models.Model):
    code = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.code


class Document_type(SoftDeleteModel, models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Document Types'
        verbose_name = 'Document Type'


class DocumentRegistration(models.Model):
    class UserType(models.IntegerChoices):
        LEGAL = 1, 'Legal Entity'
        PHYSICAL = 2, 'Physical Entity'

    phone_number = models.CharField(max_length=20)
    user_type = models.PositiveSmallIntegerField(choices=UserType.choices)
    pinfil = models.CharField(max_length=256, null=True)
    tin = models.CharField(max_length=256, null=True)
    passport_front = models.TextField()
    passport_back = models.TextField()
    licence_certificate = models.TextField(null=True)
    order_proxy = models.TextField(null=True)
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.phone_number} - {self.user_type}'

    class Meta:
        verbose_name_plural = 'Document Registrations'
        verbose_name = 'Document Registration'


class BudgetAccount(models.Model):
    code = models.CharField(max_length=30, unique=True, db_index=True)
    name = models.CharField(max_length=512)
    tin = models.IntegerField()

    def __str__(self):
        return f'{self.code} || {self.tin}'


class BudgetIncomeAccount(models.Model):
    code = models.CharField(max_length=30, unique=True, db_index=True)
    name = models.CharField(max_length=512)
    coato = models.IntegerField()
    region_code = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.code} || {self.coato} || {self.region_code}'
