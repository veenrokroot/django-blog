import re

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def username_unique_validator(username: str):
    """
    Проверка username на уникальность.
    :param username: username пользователя.
    :return:
    """
    UserModel = get_user_model()

    msg = _('Пользователь с таким username уже существует.')
    code = 'username_unique'
    try:
        UserModel.objects.get_by_natural_key(username=username)
    except UserModel.DoesNotExist:
        return None
    else:
        raise ValidationError(message=msg, code=code)


def username_characters_validator(username: str):
    """
    Проверка username на допустимые символы.
    :param username: username пользователя.
    :return:
    """
    msg = _('Username содержит недопустимые символы: {unacceptable_symbols}.')
    code = 'username_invalid'
    unacceptable_symbols = {
        char for char in username
        if not re.match(settings.USER_USERNAME_VALID_CHARACTERS_REGEX, char)
    }
    if unacceptable_symbols:
        msg = msg.format(unacceptable_symbols=', '.join(unacceptable_symbols))
        raise ValidationError(message=msg, code=code)
    return None


def username_first_symbol_validator(username: str):
    """
    Проверка первого символа username пользователя.
    :param username: username пользователя.
    :return:
    """
    msg = _('Username должен начинаться с латинской буквы или символа _')
    code = 'username_invalid'

    if not re.match(settings.USER_USERNAME_VALID_FIRST_SYMBOL_REGEX, username[0]):
        raise ValidationError(message=msg, code=code)
    return None


def username_minimum_length_validator(username: str):
    """
    Проверка на минимальную длинну username пользователя.
    :param username: Username пользователя.
    :return:
    """
    msg = _(f'Username должен содержать минимум {settings.USER_USERNAME_MINIMUM_LENGTH} символа.')
    code = 'username_invalid'
    if len(username) < settings.USER_USERNAME_MINIMUM_LENGTH:
        raise ValidationError(message=msg, code=code)
    return None


def username_maximum_length_validator(username: str):
    """
    Проверка на максимальную длинну username пользователя.
    :param username: Username пользователя.
    :return:
    """
    msg = _(f'Username должен содержать максимум {settings.USER_USERNAME_MAXIMUM_LENGTH} символа.')
    code = 'username_invalid'
    if len(username) > settings.USER_USERNAME_MAXIMUM_LENGTH:
        raise ValidationError(message=msg, code=code)
    return None


def email_unique_validator(email: str):
    """
    Проверка на уникальность E-mail пользователя.
    :param email: E-mail пользователя.
    :return:
    """
    UserModel = get_user_model()
    msg = _('Пользователь с таким E-mail уже существует')
    code = 'email_unique'
    try:
        UserModel.objects.get_by_natural_key(email=email)
    except UserModel.DoesNotExist:
        return None
    else:
        raise ValidationError(message=msg, code=code)
