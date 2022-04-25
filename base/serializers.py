from rest_framework import serializers

from base.models import User


class UserSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if attrs.get("is_employee", False) and attrs.get("is_customer", False):
            raise serializers.ValidationError(
                {"message": "choose only one role"}, code=400
            )
        if not attrs.get("is_employee", False) and not attrs.get("is_customer", False):
            raise serializers.ValidationError(
                {"message": "choose only one role"}, code=400
            )
        return super().validate(attrs)

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
