from django.urls import path
from .views import CustomLoginView, CustomLogoutView, HomeView, ProfileView, SignUpView


urlpatterns = [
    path('', HomeView, name='home'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/profile/', ProfileView, name='profile'),
]