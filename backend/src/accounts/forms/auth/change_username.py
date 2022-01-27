from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

UserModel = get_user_model()


class ChangeUsernameForm(forms.Form):
    """
    Форма смены username пользователя.
    """
    password = forms.CharField(
        label=_('Пароль'),
        widget=forms.PasswordInput()
    )
    repeat_password = forms.CharField(
        label=_('Повтор пароля'),
        widget=forms.PasswordInput()
    )
    new_username = forms.CharField(
        label=_('Новый Username'),
        widget=forms.PasswordInput()
    )

    error_messages = {
        'password_invalid': _('Неверный пароль'),
        'passwords_not_match': _('Пароли не совпадают')
    }

    class Meta:
        fields = ('password', 'repeat_password', 'new_username')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data['password']
        if self.request.user.check_password(raw_password=password):
            raise ValidationError(message=self.error_messages['password_invalid'], code='password_invalid')
        return password

    def clean_repeat_password(self):
        password = self.cleaned_data['password']
        repeat_password = self.cleaned_data['repeat_password']

        if password != repeat_password:
            raise ValidationError(message=self.error_messages['passwords_not_match'], code='passwords_not_match')
        return repeat_password

    def clean_new_username(self):
        new_username = self.cleaned_data['new_username']
        user = self.request.user
        user.username = new_username
        user.clean()
        return new_username

    def save(self):
        new_username = self.cleaned_data['new_username']
        user = self.request.user
        user.username = new_username
        user.save()
