from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from base.models import User


@receiver(post_save, sender=User)
def generate_auth_token(instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
