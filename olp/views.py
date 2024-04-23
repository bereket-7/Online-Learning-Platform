# views.py

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
class HomeView():
    template_name = 'templates/home.html'
    
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('profile')

class CustomLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'accounts/logout.html'
    
class ProfileView(LoginRequiredMixin):
    template_name = 'accounts/profile.html'

class SignUpView(CreateView):
    model = User
    template_name = 'accounts/signup.html'
    fields = ['username', 'email', 'password']
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)
