from rest_framework import serializers

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """Full user serializer — excludes password."""

    class Meta:
        model = CustomUser
        exclude = ("password",)
        read_only_fields = ("id", "date_joined", "last_login")


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new users (password is write-only)."""

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "user_type",
            "school",
            "password",
        )
        read_only_fields = ("id",)

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserMinimalSerializer(serializers.ModelSerializer):
    """Lightweight serializer used in nested / list contexts."""

    class Meta:
        model = CustomUser
        fields = ("id", "email", "first_name", "last_name", "user_type")
        read_only_fields = fields
