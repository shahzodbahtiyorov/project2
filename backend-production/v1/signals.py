from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from v1.models.users import AccessToken

User = get_user_model()


@receiver(post_save, sender=User)
def create_access_token(sender, instance, created, **kwargs):
    if created:
        access_token = AccessToken(user=instance)
        access_token.generate()
