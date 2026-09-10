from django.urls import path

from .views import (
    ChangePasswordView,
    CustomLoginView,
    HomePageView,
    LogoutPage,
    PasswordResetConfirmPage,
    PasswordResetDonePage,
    PasswordResetRequestView,
    ProfileView,
    RegisterPage,
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', LogoutPage.as_view(), name='logout'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset/done/', PasswordResetDonePage.as_view(), name='password_reset_done'),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        PasswordResetConfirmPage.as_view(),
        name='password_reset_confirm',
    ),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]
