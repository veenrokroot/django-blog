from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView

from src.accounts import forms


class ChangePasswordView(LoginRequiredMixin, FormView):
    """
    Страница смены password пользователя.
    """
    template_name = 'accounts/account/change-password.html'
    form_class = forms.auth.ChangeUsernameForm
    success_url = settings.LOGOUT_REDIRECT_URL

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.save()
        logout(self.request)
        return super().form_valid(form)
