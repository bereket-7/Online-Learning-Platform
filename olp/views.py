# views.py
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic.edit import FormView

from django.contrib.auth import logout, login,update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView

from django.views import View
from .forms.registration_form import CustomUserCreationForm 


class ProfileView(View):
    def get(self, request):
        return render(request, 'account/profile.html')

class HomePageView(View):
    def get(self, request):
        return render(request, 'home.html')
    
class CustomLoginView(LoginView):
    template_name = 'account/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('profile')

class RegisterPage(FormView):
    template_name = 'account/signup.html'
    form_class = CustomUserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('register')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    
class LogoutPage(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('home')
    

class PasswordResetRequestView(PasswordResetView):
    template_name = 'account/password_reset_request.html'
    success_url = reverse_lazy('password_reset_done')
    email_template_name = 'account/password_reset_email.html'
    form_class = PasswordResetForm

class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('login')
    form_class = SetPasswordForm
    
class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'account/change_password.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        self.user = form.save()
        update_session_auth_hash(self.request, self.user)
        return super().form_valid(form)