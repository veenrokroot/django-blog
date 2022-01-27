from django.conf import settings
from django.views.generic import FormView
from src.accounts import forms
from src.accounts.mixins.logout_required import LogoutRequiredMixin


class SignUpView(LogoutRequiredMixin, FormView):
    """
    Страница регистрации пользователя.
    """
    template_name = 'accounts/auth/sign-up.html'
    form_class = forms.auth.SignUpForm
    success_url = settings.LOGIN_URL

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
