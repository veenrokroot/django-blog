from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

UserModel = get_user_model()


class ChangePasswordForm(forms.Form):
    """
    Форма смены username пользователя.
    """
    old_password = forms.CharField(
        label=_('Старый пароль'),
        widget=forms.PasswordInput()
    )
    new_password = forms.CharField(
        label=_('Новый пароль'),
        widget=forms.PasswordInput()
    )
    repeat_new_password = forms.CharField(
        label=_('Повтор пароля'),
        widget=forms.PasswordInput()
    )

    error_messages = {
        'password_invalid': _('Неверный пароль'),
        'passwords_not_match': _('Пароли не совпадают'),
        'new_password_equal_old_password': _('Новый пароль совпадает со старым')
    }

    class Meta:
        fields = ('old_password', 'new_password', 'repeat_new_password')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.request.user.check_password(raw_password=old_password):
            raise ValidationError(message=self.error_messages['password_invalid'], code='password_invalid')
        return old_password

    def clean_repeat_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        repeat_new_password = self.cleaned_data.get('repeat_new_password')
        if new_password != repeat_new_password:
            raise ValidationError(message=self.error_messages['passwords_not_match'], code='passwords_not_match')

        return repeat_new_password

    def clean_new_password(self):
        old_password = self.cleaned_data.get('old_password')
        new_password = self.cleaned_data.get('new_password')
        if new_password == old_password:
            raise ValidationError(
                message=self.error_messages['new_password_equal_old_password'],
                code='new_password_equal_old_password'
            )

        validate_password(password=new_password)
        return new_password

    def save(self):
        new_password = self.cleaned_data['new_password']
        self.request.user.set_password(raw_password=new_password)
        self.request.user.save()
