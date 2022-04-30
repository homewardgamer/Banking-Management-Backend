from rest_framework import serializers
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password

from base.models import *


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "address",
            "dob",
            "is_customer",
            "is_employee",
            "branch",
        ]

    def validate(self, attrs):
        if (
            self.context["request"].user.is_authenticated
            and self.context["request"].user.is_employee
        ):
            attrs["is_employee"] = True
            attrs["is_customer"] = False
        if attrs.get("is_employee", False) and attrs.get("is_customer", False):
            raise serializers.ValidationError(
                {"message": "choose only one role"}, code=400
            )
        if not attrs.get("is_employee", False) and not attrs.get("is_customer", False):
            raise serializers.ValidationError(
                {"message": "choose only one role"}, code=400
            )
        password_validation.validate_password(attrs["password"])
        attrs["password"] = make_password(attrs["password"])
        return super().validate(attrs)


class TransactionSerializer(serializers.ModelSerializer):
    pin = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = Transaction
        fields = "__all__"

    def validate(self, attrs):
        deposit = Transaction.TransactionTypes.DEPOSIT
        withdraw = Transaction.TransactionTypes.WITHDRAW
        transfer = Transaction.TransactionTypes.TRANSFER

        # Check correct combination of data
        combination = (
            attrs["type"],
            attrs.get("r_account", None),
            attrs.get("s_account", None),
        )
        if not (
            (combination[0] == deposit and combination[1] and not combination[2])
            or (combination[0] == withdraw and not combination[1] and combination[2])
            or (combination[0] == transfer and combination[1] and combination[2])
        ):
            raise serializers.ValidationError(
                {"detail": "invalid (type, r_account, s_account) combination"}, code=400
            )

        # Check pin
        if attrs["type"] in [transfer, withdraw]:
            actual_pin = attrs["s_account"].pin
            provided_pin = attrs["pin"]
            if provided_pin != actual_pin:
                raise serializers.ValidationError({"failed": "incorrect pin"}, code=400)
        if attrs["type"] == deposit:
            actual_pin = attrs["r_account"].pin
            provided_pin = attrs["pin"]
            if provided_pin != actual_pin:
                raise serializers.ValidationError({"failed": "incorrect pin"}, code=400)

        # Check for account state (enabled/disabled)
        if attrs["type"] == transfer:
            if attrs["s_account"].disabled or attrs["r_account"].disabled:
                raise serializers.ValidationError(
                    {"detail": "one of the account is disabled"}, code=400
                )
        if attrs["type"] == deposit:
            if attrs["r_account"].disabled:
                raise serializers.ValidationError(
                    {"detail": "account is disabled"}, code=400
                )
        if attrs["type"] == withdraw:
            if attrs["s_account"].disabled:
                raise serializers.ValidationError(
                    {"detail": "account is disabled"}, code=400
                )

        # Check if sender account contains sufficient balance
        if attrs["type"] in [withdraw, transfer]:
            s_account = attrs["s_account"]
            if s_account.balance - attrs["amount"] < 0:
                raise serializers.ValidationError(
                    {"amount": "insufficient balance"}, code=400
                )

        del attrs["pin"]

        return super().validate(attrs)


class AccountSerializer(serializers.ModelSerializer):
    pin = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = Account
        fields = "__all__"

    def validate(self, attrs):
        pin = attrs["pin"]
        if len(pin) != 4 and not pin.isdigit():
            raise serializers.ValidationError({"pin": "invalid pin"})
        return super().validate(attrs)


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "address",
            "dob",
        ]


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirm = serializers.CharField(required=True)

    model = User

    def validate(self, attrs):
        new_password = attrs["new_password"]
        new_password_confirm = attrs["new_password_confirm"]
        if new_password != new_password_confirm:
            raise serializers.ValidationError(
                {"detail": "new_password fields must match"}, code=400
            )
        password_validation.validate_password(new_password)
        return attrs
