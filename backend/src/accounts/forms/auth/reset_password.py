from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

UserModel = get_user_model()


class ResetPasswordForm(forms.Form):
    """
    Форма сброса пароля пользователя.
    """
    email = forms.EmailField(
        label=_('E-mail'),
    )
    message_errors = {
        'user_not_exist': _('Пользователя с данным E-mail не существует.')
    }

    class Meta:
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        self.user: UserModel = None
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            self.user = UserModel.objects.get_by_natural_key(email=email)
        except UserModel.DoesNotExist:
            raise ValidationError(message=self.message_errors['user_not_exist'], code='user_not_exist')

    def get_user(self):
        return self.user
