from django.db import models

from v1.models import Users


class ClientInfo(models.Model):
    branch_code = models.CharField(max_length=100)
    branch_name = models.CharField(max_length=256)
    devision_code = models.CharField(max_length=100)
    devision_name = models.CharField(max_length=256)
    client_code = models.CharField(max_length=100, unique=True)
    client_name = models.CharField(max_length=256)
    direction_code = models.CharField(max_length=100)
    direction_name = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    country = models.CharField(max_length=256)
    locality = models.CharField(max_length=256)
    org_unit = models.CharField(max_length=256)
    state = models.CharField(max_length=256)
    tin = models.CharField(max_length=256)
    user = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    contract_date = models.DateField()
    contract_number = models.CharField(max_length=100, unique=True)
    director = models.CharField(max_length=100)
    accountant = models.CharField(max_length=100)
    has_password = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.client_code} -- {self.client_name} '


class ClientCertificate(models.Model):
    client = models.ForeignKey(ClientInfo, on_delete=models.DO_NOTHING)
    otp_code = models.BigIntegerField(null=True, blank=True)
    pin_code = models.CharField(max_length=100, null=True, blank=True)
    cms = models.CharField(max_length=2500, null=True, blank=True)

    def __str__(self):
        return f'cert owner || {self.client.user.username} ||'
