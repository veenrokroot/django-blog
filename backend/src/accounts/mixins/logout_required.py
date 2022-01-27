from django.shortcuts import redirect


class LogoutRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:sign-out')
        return super().dispatch(request, *args, **kwargs)