from rest_framework import serializers
from django.contrib.auth import password_validation, authenticate
from .models import User
from bot.utils import validate_incoming_data
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {"refresh": str(refresh), "access": str(refresh.access_token), "id": user.id}


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ("email", "password", "confirm_password", "phone")
        extra_kwargs = {
            "email": {"required": False},
            "password": {"required": False},
            "phone": {"required": False},
        }

    def validate(self, data):
        errors = validate_incoming_data(data, list(self.fields.keys()))

        if errors:
            raise serializers.ValidationError({"error": errors})

        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError(
                {"error": "Password and confirm_password are not the same."}
            )
        password_validation.validate_password(password)
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password", None)
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    def validate(self, data):
        request = self.context.get("request")

        errors = validate_incoming_data(data, list(self.fields.keys()))

        user = authenticate(request, **data)
        if not user:
            errors.append({"error": "Invalid credentials"})

        if errors:
            raise serializers.ValidationError({"error": errors})

        tokens = get_tokens_for_user(user)
        data["tokens"] = tokens

        return data

    class Meta:
        model = User
        fields = ("email", "password")
        extra_kwargs = {
            "email": {"required": False},
            "password": {"write_only": True, "required": False},
        }
