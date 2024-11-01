from rest_framework import serializers
from django.contrib.auth import password_validation
from .models import User
from bot.utils import validate_incoming_data


class UserSerializer(serializers.Serializer):
    confirm_password = serializers.CharField(
        validators=password_validation, write_only=True
    )
    password = serializers.CharField(validators=password_validation, write_only=True)

    class Meta:
        model = User
        fields = ("email", "password", "confirm_password", "phone")
        read_only_fields = ("email", "phone")

    def validate(self, data):
        errors = validate_incoming_data(data, self.fields.keys())

        if errors:
            raise serializers.ValidationError({"error": errors})

        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError(
                {"error": "Password and confirm_password are not the same."}
            )

        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
