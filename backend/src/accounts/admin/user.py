from django.contrib import admin
from src.accounts import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    """
    Настройки администрирования пользователей.
    """
    list_display = (
        '__str__',
        'id',
        models.User.USERNAME_FIELD,
        models.User.EMAIL_FIELD,
    )
    list_display_links = (
        '__str__',
    )
    list_filter = (
        'is_superuser',
        'is_staff',
        'is_active',
    )
    search_fields = (
        'id',
        models.User.USERNAME_FIELD,
        models.User.EMAIL_FIELD,
    )
