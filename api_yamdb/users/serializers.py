from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.core.validators import RegexValidator
from users.models import User
from users.validators import valid_username


class TokenSerializer(serializers.Serializer):
    """Сериализатор для запросто /auth/token."""
    username = serializers.CharField(max_length=150, write_only=True)
    confirmation_code = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        """Проверка пользователя и генерация токена."""
        username = data.get('username', None)
        confirmation_code = data.get('confirmation_code', None)
        user = get_object_or_404(User, username=username)
        if not user.confirmation_code == confirmation_code:
            raise ValidationError(
                (
                    'Пользователь с таким именем '
                    'и проверочным кодом не найден.'
                )
            )
        if not user.is_active:
            raise serializers.ValidationError(
                'Этот пользователь заблокирован.'
            )

        return user


class SignupSerializer(serializers.Serializer):
    """Сериализатор для запросто /auth/signup."""
    username = serializers.CharField(
        max_length=150,
        validators=[
            RegexValidator(regex=r'^[\w.@+-]+$'),
            valid_username,
        ],
        required=True
    )
    email = serializers.EmailField(
        max_length=254,
        required=True
    )

    def validate(self, data):
        username = data.get('username', None)
        email = data.get('email', None)
        if User.objects.filter(
            username=username,
            email=email
        ).exists():
            return data
        if User.objects.filter(
            username=username
        ).exists():
            raise ValidationError(
                {
                    'Username': [
                        "Пользователь уже существует."
                    ]
                }
            )
        if User.objects.filter(
            email=email
        ).exists():
            raise ValidationError(
                {
                    'Email': [
                        "Email уже существует."
                    ]
                }
            )
        return data

    def create(self, validated_data):
        current_user = User.objects.create_user(**validated_data)
        return current_user
