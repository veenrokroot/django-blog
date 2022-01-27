from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

UserModel = get_user_model()


class SignInForm(forms.ModelForm):
    """
    Форма авторизации пользователя.
    """
    login = forms.CharField(
        label=_('E-mail или Username'),
        help_text=_('Обязательно.'),
        empty_value=_('Введите свой E-mail или Username.')
    )
    error_messages = {
        'login_invalid': _('Не верный логин или пароль.'),
    }

    class Meta:
        model = UserModel
        fields = ('login', 'password',)

    def __init__(self, *args, **kwargs):
        self.user_cache: UserModel = None
        self.request: HttpRequest = kwargs.pop('request')

        super().__init__(*args, **kwargs)

    def clean(self):
        login = self.cleaned_data['login']
        password = self.cleaned_data['password']

        self.user_cache = authenticate(self.request, username=login, password=password)

        if self.user_cache is None or not self.user_cache.is_authenticated:
            self.user_cache = authenticate(self.request, email=login, password=password)

            if self.user_cache is None or not self.user_cache.is_authenticated:
                raise ValidationError(message=self.error_messages['login_invalid'], code='login_invalid')
        return super().clean()

    def get_user(self):
        return self.user_cache
