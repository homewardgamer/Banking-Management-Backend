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


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"
