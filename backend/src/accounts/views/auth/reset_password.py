from django.conf import settings
from django.views.generic import FormView

from src.accounts import forms


class ResetPasswordView(FormView):
    """
    Страница сброса пароля.
    """
    template_name = 'accounts/auth/reset-password.html'
    form_class = forms.auth.ResetPasswordForm
    success_url = settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        user = form.get_user()
        # Логика отправки ссылки для сброса пароля
        return super().form_valid(form)
