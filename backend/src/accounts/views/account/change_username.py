from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView

from src.accounts import forms


class ChangeUsernameView(LoginRequiredMixin, FormView):
    """
    Страница смены username пользователя.
    """
    template_name = 'accounts/account/change-username.html'
    form_class = forms.account.ChangeUsernameForm
    success_url = reverse_lazy('accounts:settings')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
