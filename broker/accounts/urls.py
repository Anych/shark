from django.urls import path

from accounts.views import (
    RegisterView,
    LoginView,
    LogoutView,
    ConfirmAccountView,
    ForgotPasswordView,
    ResetPasswordValidateView,
    ResetPasswordView,
    ChangePasswordView,
    ConfirmEmailView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('confirm-email/', ConfirmEmailView.as_view(), name='confirm_email'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),

    path('activate/<uidb64>/<token>/<email>/<command>', ConfirmAccountView.as_view(), name='activate'),
    path('reset_password_validate/<uidb64>/<token>/',
         ResetPasswordValidateView.as_view(),
         name='reset_password_validate'),
]