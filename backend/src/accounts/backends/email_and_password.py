from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

UserModel = get_user_model()


class EmailCaseInsensitiveAndPasswordBackendAuthentication(ModelBackend):
    """
    Аунтетификация пользователя по E-mail, не чувствительному к регистру и паролю.
    """
    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None:
            email = kwargs.get(UserModel.EMAIL_FIELD, None)
        if email is None or password is None:
            return None

        try:
            user = UserModel.objects.get_by_natural_key(email=email)
        except UserModel.DoesNotExist:
            return None
        except UserModel.UserModel.MultipleObjectsReturned:
            return None
        else:
            if not user.check_password(raw_password=password):
                return None
            elif not self.user_can_authenticate(user=user):
                return None
            else:
                return user
