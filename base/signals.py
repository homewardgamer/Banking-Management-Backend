from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from base.models import User, Transaction


@receiver(post_save, sender=User)
def generate_auth_token(instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=Transaction)
def modify_account_balance(instance=None, created=False, **kwargs):
    if created:
        if instance.s_account:
            instance.s_account.balance -= instance.amount
            instance.s_account.save()
        if instance.r_account:
            instance.r_account.balance += instance.amount
            instance.r_account.save()
