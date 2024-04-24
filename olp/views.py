# views.py
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic.edit import FormView
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.views import View
from .registration_form import CustomUserCreationForm 
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