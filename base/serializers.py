from rest_framework import serializers

from base.models import User


class UserSerializer(serializers.ModelSerializer):
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
