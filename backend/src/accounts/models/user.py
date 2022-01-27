from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from src.accounts import validators


class UserManager(DjangoUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        UserModel = get_user_model()
        username = UserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username: str = None, email: str = None):
        assert username is not None or email is not None, ValueError('Username or E-mail is not None')
        if username is not None:
            return self.get(**{f'{self.model.USERNAME_FIELD}__iexact': username})
        elif email is not None:
            return self.get(**{f'{self.model.EMAIL_FIELD}__iexact': email})


class User(AbstractBaseUser, PermissionsMixin):
    """
    Model User.
    """
    username = models.CharField(
        verbose_name=_('Username'),
        help_text=_('Обязательно.'),
        unique=True,
        max_length=settings.USER_USERNAME_MAXIMUM_LENGTH,
        validators=(
            validators.user.username_minimum_length_validator,
            validators.user.username_maximum_length_validator,
            validators.user.username_first_symbol_validator,
            validators.user.username_characters_validator,
            validators.user.username_unique_validator,
        ),
        error_messages={
            'max_length': None,
            'unique': None
        }
    )
    email = models.EmailField(
        verbose_name=_('E-mail'),
        help_text=_('Обязательно.'),
        validators=(
            validators.user.email_unique_validator,
        ),
        error_messages={
            'unique': None,
        }
    )

    is_staff = models.BooleanField(
        verbose_name=_('Статус персонала'),
        help_text=_('Можно настроить доступ к админ-панеле сайта')
    )
    is_active = models.BooleanField(
        verbose_name=_('Активирован'),
        help_text=_('Используйте данное поле для деактивации аккаунта, вместо удаления.'),
        default=True
    )

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = (
        EMAIL_FIELD,
    )

    objects = UserManager()

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        ordering = ('username',)

    def __str__(self):
        return f'{self.username}'
