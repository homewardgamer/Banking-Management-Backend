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
        ]

    def validate(self, attrs):
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
    class Meta:
        model = Transaction
        fields = "__all__"

    def validate(self, attrs):
        deposit = Transaction.TransactionTypes.DEPOSIT
        withdraw = Transaction.TransactionTypes.WITHDRAW
        transfer = Transaction.TransactionTypes.TRANSFER
        combination = (
            attrs["type"],
            attrs.get("r_account", None),
            attrs.get("s_account", None),
        )
        if combination[0] == deposit and combination[1] and not combination[2]:
            return super().validate(attrs)
        if combination[0] == withdraw and not combination[1] and combination[2]:
            return super().validate(attrs)
        if combination[0] == transfer and combination[1] and combination[2]:
            return super().validate(attrs)
        raise serializers.ValidationError(
            {"detail": "invalid (type, r_account, s_account) combination"}, code=400
        )


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"
