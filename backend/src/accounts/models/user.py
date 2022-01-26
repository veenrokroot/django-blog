from django.apps import apps
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.core.validators import MinLengthValidator
from django.db import models
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
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        UserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        username = UserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username: str = None, email: str = None):
        assert username is not None or email is not None
        if username is not None:
            return self.get(**{self.model.USERNAME_FIELD: username})
        elif email is not None:
            return self.get(**{self.model.EMAIL_FIELD: email})


class User(AbstractBaseUser, PermissionsMixin):
    """
    Model User.
    """
    username = models.CharField(
        verbose_name=_('Username'),
        help_text=_('Обязательно.'),
        max_length=32,
        validators=(
            validators.user.username_minimum_length_validator,
            validators.user.username_minimum_length_validator,
            validators.user.username_first_symbol_validator,
            validators.user.username_characters_validator,
            validators.user.username_unique_validator,
        )
    )
    email = models.EmailField(
        verbose_name=_('E-mail'),
        help_text=_('Обязательно.'),
        validators=(
            validators.user.email_unique_validator,
        )
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
