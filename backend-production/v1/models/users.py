import datetime
import pytz
import uuid
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from v1.models.manager import CustomUserManager
from v1.models.session import Session
from django_softdelete.models import SoftDeleteModel

utc = pytz.UTC


def on_delete_session(instance):
    print(isinstance(AccessToken, instance))


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    comment = models.CharField(max_length=255, blank=True)
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Permission(models.Model):
    name = models.CharField(max_length=50, unique=True)
    comment = models.CharField(max_length=255, blank=True)
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.role.name)

    class Meta:
        unique_together = ('role', 'permission')
        verbose_name = "Role Permission"
        verbose_name_plural = "Role Permissions"


class Users(SoftDeleteModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), unique=True, max_length=50)
    phone_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    avatar = models.CharField(max_length=255, null=True, blank=True)
    is_sms = models.BooleanField(default=False)
    birth_date = models.DateField(null=True, blank=True)
    salary = models.FloatField(null=True, blank=True)
    is_test = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    identity = models.CharField(max_length=3, default='TT')
    permissions = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    workspace = models.ForeignKey('ClientInfo', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number']

    class Meta:
        verbose_name_plural = "👤Users"

    objects = CustomUserManager()


class AccessToken(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="access_token")
    key = models.CharField(max_length=128)
    session = models.ForeignKey(Session, on_delete=models.SET(on_delete_session), null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def generate(self):
        self.key = f"{uuid.uuid4()}/{uuid.uuid4()}"

        self.save()
        return self.key

    def __str__(self):
        return self.user.username


class Service:
    pass


class UsersServicePermissions:
    pass


class ExpiredAccessToken(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="expired_access_token")
    key = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class IPAddress(models.Model):
    ip_address = models.CharField(max_length=45)
    timestamp = models.DateTimeField(auto_now_add=True)


class IPBlackList(models.Model):
    ip_address = models.CharField(max_length=45)
    blocked_at = models.DateTimeField()
    blocked_time = models.IntegerField(default=10)

    @property
    def is_blocked(self):
        delta = datetime.datetime.utcnow().replace(tzinfo=utc) - self.blocked_at
        if int(delta.total_seconds() // 60) < self.blocked_time:
            return True
        return False

    @property
    def left_time(self):
        if self.is_blocked:
            delta = datetime.datetime.utcnow().replace(tzinfo=utc) - self.blocked_at
            return self.blocked_time * 60 - round(delta.total_seconds())
        return 0


class IPMiddleware(models.Model):
    requests_count = models.IntegerField(default=1000)
    requests_time = models.IntegerField(default=1, help_text="hour")
    block_time = models.IntegerField(default=10, help_text="minute")


class BlackList(SoftDeleteModel, models.Model):
    name = models.CharField(max_length=128, null=True)
    transfer_type = models.IntegerField(default=0, null=True)
    number = models.CharField(max_length=125)
    daily = models.BooleanField(default=False)
    monthly = models.BooleanField(default=False)
    permanent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class WhiteList(SoftDeleteModel, models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="white", null=True)
    type = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class Limits(models.Model):
    name = models.CharField(max_length=128)
    transfer_type = models.IntegerField(default=0)
    daily_amount = models.FloatField(max_length=50)
    daily_amount_white = models.FloatField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
