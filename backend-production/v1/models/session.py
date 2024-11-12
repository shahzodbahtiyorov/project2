import datetime
from api import settings
from django.db import models


class Session(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="session")
    name = models.CharField('Device name', max_length=100, null=True)
    uuid = models.CharField('Device uuid', max_length=50)
    revoke = models.IntegerField('Revoke')
    block = models.IntegerField('Block')
    primary = models.IntegerField('Primary', default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def collection(self):
        return {
            'id': self.id,
            'name': self.name,
            'uuid': self.uuid,
            'created_at': (self.created_at + datetime.timedelta(hours=5)).strftime("%d.%m.%Y %H:%M:%S"),
            'updated_at': (self.updated_at + datetime.timedelta(hours=5)).strftime("%d.%m.%Y %H:%M:%S"),
        }

    class Meta:
        verbose_name_plural = "11. Session"

