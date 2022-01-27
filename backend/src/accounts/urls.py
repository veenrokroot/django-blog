from django.urls import path

from src.accounts import views

app_name = 'accounts'

urlpatterns = (
    path('change_password/', views.account.ChangePasswordView.as_view(), name='change-password'),
    path('change_username/', views.account.ChangeUsernameView.as_view(), name='change-username'),

    path('auth/sign-out', views.auth.SignOutView.as_view(), name='sign-out'),
    path('auth/sign-in', views.auth.SignInView.as_view(), name='sign-in'),
    path('auth/sign-up', views.auth.SignUpView.as_view(), name='sign-up'),
    path('auth/reset-password', views.auth.ResetPasswordView.as_view(), name='reset-password'),
)
