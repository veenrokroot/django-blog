from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

UserModel = get_user_model()


class UsernameCaseInsensitiveAndPasswordBackendAuthentication(ModelBackend):
    """
    Аунтетификация пользователя по username, не чувствительному к регистру и паролю.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD, None)
        if username is None or password is None:
            return None

        try:
            user = UserModel.objects.get_by_natural_key(username=username)
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
