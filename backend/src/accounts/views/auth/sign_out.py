from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class SignOutView(LoginRequiredMixin, TemplateView):
    """
    Страница выхода пользователя.
    """
    template_name = 'accounts/auth/sign-out.html'
    success_url = settings.LOGOUT_REDIRECT_URL

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)
