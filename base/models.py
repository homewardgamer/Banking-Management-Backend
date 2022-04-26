from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Branch(models.Model):
    branch_id = models.BigAutoField(primary_key=True)
    branch_name = models.CharField(max_length=300)
    branch_address = models.CharField(max_length=500)
    branch_code = models.IntegerField(unique=True)


class User(AbstractUser):
    address = models.CharField(_("address"), max_length=300, blank=True)
    dob = models.DateField(_("dob"), null=True)
    is_customer = models.BooleanField(_("is_customer"), default=False)
    is_employee = models.BooleanField(_("is_employee"), default=False)
    updated_at = models.DateTimeField(auto_now=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)


class Account(models.Model):
    account_id = models.BigAutoField(primary_key=True)
    account_holder = models.ForeignKey(User, on_delete=models.CASCADE)
    account_type = models.CharField(
        _("account_type"), max_length=300, default="savings"
    )
    balance = models.DecimalField(
        _("balance"), decimal_places=2, max_digits=10, default=0.0
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Transaction(models.Model):
    class TransactionTypes(models.TextChoices):
        DEPOSIT = "DEPOSIT", "Deposit"
        WITHDRAW = "WITHDRAW", "Withdraw"
        TRANSFER = "TRANSFER", "Transfer"

    transaction_id = models.BigAutoField(primary_key=True)
    r_account = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, related_name="r_transactions"
    )
    s_account = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, related_name="s_transactions"
    )
    type = models.CharField(max_length=300, choices=TransactionTypes.choices)
    amount = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)
