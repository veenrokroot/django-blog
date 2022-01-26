from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.accounts'
    app_label = 'accounts'
    verbose_name = _('Accounts and Authentications')
