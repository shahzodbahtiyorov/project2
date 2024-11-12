from django.db import models


class Client(models.Model):
    org_name = models.CharField(max_length=100, unique=True)
    certificate = models.JSONField()

    def __str__(self):
        return self.org_name
