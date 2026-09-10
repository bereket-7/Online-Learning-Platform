from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import FormView

from .forms.registration_form import CustomUserCreationForm


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        profile = getattr(request.user, 'profile', None)
        context = {
            'user': request.user,
            'profile': profile,
        }
        return render(request, 'account/profile.html', context)


class HomePageView(View):
    def get(self, request):
        return render(request, 'home.html')


class CustomLoginView(LoginView):
    template_name = 'account/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('profile')


class RegisterPage(FormView):
    template_name = 'account/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('profile')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class LogoutPage(LoginRequiredMixin, View):
    def post(self, request):
        logout(request)
        return redirect('home')

    def get(self, request):
        # Prefer POST logout; keep GET as a soft redirect for old links.
        return redirect('home')


class PasswordResetRequestView(PasswordResetView):
    template_name = 'account/password_reset_request.html'
    success_url = reverse_lazy('password_reset_done')
    email_template_name = 'account/password_reset_email.html'
    form_class = PasswordResetForm


class PasswordResetDonePage(PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class PasswordResetConfirmPage(PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('login')
    form_class = SetPasswordForm


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'account/change_password.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        response = super().form_valid(form)
        update_session_auth_hash(self.request, form.user)
        return response
