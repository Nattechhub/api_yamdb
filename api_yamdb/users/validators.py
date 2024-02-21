from django.core.exceptions import ValidationError


def valid_username(value):
    """Запрещает создание пользователя с username == me."""
    if value == 'me':
        raise ValidationError(
            'Имя пользователя me не допустимо'
        )
    return value
