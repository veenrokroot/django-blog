from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

UserModel = get_user_model()


class SignUpForm(forms.ModelForm):
    """
    Форма регистрации пользователя.
    """
    repeat_password = forms.CharField(
        label=_('Повтор пароля'),
        widget=forms.PasswordInput()
    )

    error_messages = {
        'passwords_not_match': _('Пароли не совпадают')
    }

    class Meta:
        model = UserModel
        fields = (UserModel.USERNAME_FIELD, UserModel.EMAIL_FIELD, 'password', 'repeat_password')

    def clean_repeat_password(self):
        password = self.cleaned_data['password']
        repeat_password = self.cleaned_data['repeat_password']

        if password != repeat_password:
            raise ValidationError(message=self.error_messages['passwords_not_match'], code='passwords_not_match')

    def save(self, *args, **kwargs):
        username = self.cleaned_data[UserModel.USERNAME_FIELD]
        email = self.cleaned_data[UserModel.EMAIL_FIELD]
        password = self.cleaned_data['password']

        return UserModel.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
