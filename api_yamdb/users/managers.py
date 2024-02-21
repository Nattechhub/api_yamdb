from django.contrib.auth.base_user import BaseUserManager
from django.utils.crypto import get_random_string


class CustomUserManager(BaseUserManager):
    """
    Кастомная модель менеджера пользователей.
    Изменены функции для создания пользователей.
    Добавлена генерация пароля при его отсутствии в запросе.
    Добавлена генерация кода подтверждения.
    """
    CODE_LENGTH = 40
    PASS_LENGTH = 15

    def _generate_random_string(self, length):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        secret_key = get_random_string(length, chars)
        return secret_key

    def _create_user(self, username, email, password, **extra_fields):
        """
        Создание пользователя.
        """
        if not username:
            raise ValueError('Необходимо указать имя пользователя.')
        if email is None:
            raise TypeError('Необходимо указать email адрес.')
        if password is None:
            password = self._generate_random_string(self.PASS_LENGTH)
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        confirmation_code = self._generate_random_string(self.CODE_LENGTH)
        user = self.model(
            username=username,
            email=email,
            confirmation_code=confirmation_code,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        Создание обычного пользователя.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Создание суперпользователя пользователя.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'У Суперюзера параметр должен быть is_staff=True.'
            )
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'У Суперюзера параметр должен быть is_superuser=True.'
            )

        return self._create_user(username, email, password, **extra_fields)
