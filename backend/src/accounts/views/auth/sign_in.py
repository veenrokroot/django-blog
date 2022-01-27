from django.conf import settings
from django.contrib.auth import login
from django.views.generic import FormView

from src.accounts import forms
from src.accounts.mixins.logout_required import LogoutRequiredMixin


class SignInView(LogoutRequiredMixin, FormView):
    """
    Страница входа пользователя.
    """
    template_name = 'accounts/auth/sign-in.html'
    form_class = forms.auth.SignInForm
    success_url = settings.LOGIN_REDIRECT_URL

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)
