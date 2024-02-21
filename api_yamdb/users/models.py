from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework_simplejwt.tokens import RefreshToken
from .managers import CustomUserManager
from .validators import valid_username


class User(AbstractBaseUser, PermissionsMixin):
    """Модель для расширения встроенного класса User."""
    username_validator = UnicodeUsernameValidator()

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )

    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        help_text=(
            'Обязательно. Длинна не более 150 символов.'
            'Буквы, цифры и @/./+/-/_ .'
        ),
        validators=[username_validator, valid_username],
        error_messages={
            'unique': ("Такой пользователь уже существует."),
        },
    )
    first_name = models.CharField('Имя', max_length=30, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
    role = models.CharField(
        'Роль пользователя',
        max_length=10,
        choices=ROLES,
        default="user"
    )
    bio = models.TextField(
        'Биография',
        blank=True,
        null=True,
    )
    email = models.EmailField(
        'email address',
        max_length=254,
        unique=True
    )
    confirmation_code = models.CharField(
        max_length=128,
        blank=True
    )

    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text=(
            'Определяет, может ли пользователь'
            'входить в панель администратора..'
        ),
    )
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text=(
            'Определяет является ли пользователь активным. '
            'Можно использовать для блокировки.'
        ),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(
        'Дата присоединения',
        default=timezone.now
    )

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    @property
    def token(self):
        """Возвращает токен доступа для пользователя."""
        return self._get_tokens_for_user()

    def get_full_name(self):
        """Возвращает полное имя пользователя."""
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Возвращает короткое имя пользователя."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def send_confirmation_code(self):
        """Высылает пользователю код подтверждения для пользователя."""
        self.email_user(
            subject=f'Conformation code for {self.username}',
            message=(
                f'Your conformation code:\n\n Code: {self.confirmation_code}'
            )
        )

    def _get_tokens_for_user(self):
        refresh = RefreshToken.for_user(self)
        return str(refresh.access_token)

    @property
    def is_user(self):
        """Возвращает True, если роль user."""
        return self.role == self.USER

    @property
    def is_moderator(self):
        """Возвращает True, если роль moderator."""
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        """Возвращает True, если роль admin."""
        return self.role == self.ADMIN
