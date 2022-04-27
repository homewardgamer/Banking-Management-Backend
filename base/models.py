from django.contrib.auth.models import AbstractUser
from django.db import models


class Branch(models.Model):
    branch_id = models.BigAutoField(primary_key=True)
    branch_name = models.CharField(max_length=300)
    branch_address = models.CharField(max_length=500)
    branch_code = models.IntegerField(unique=True)

    class Meta:
        verbose_name_plural = "branches"

    def __str__(self) -> str:
        return f"{self.branch_code} {self.branch_name}"


class User(AbstractUser):
    address = models.CharField(max_length=300, blank=True)
    dob = models.DateField(null=True)
    is_customer = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)


class Account(models.Model):
    class AccountTypes(models.TextChoices):
        SAVING = "SAVING", "Saving"
        CURRENT = "CURRENT", "Current"

    account_id = models.BigAutoField(primary_key=True)
    account_holder = models.ForeignKey(User, on_delete=models.CASCADE)
    account_type = models.CharField(
        max_length=300, default=AccountTypes.SAVING, choices=AccountTypes.choices
    )
    balance = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.account_id} {self.account_holder.username} ({self.account_type})"


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

    def __str__(self) -> str:
        return f"{self.transaction_id} ({self.type})"
