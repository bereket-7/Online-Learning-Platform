"""
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .views import CustomLoginView, HomePageView, LogoutPage, ProfileView, RegisterPage

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/',RegisterPage.as_view(), name='register'),
    path('profile/',ProfileView.as_view(), name='profile'),
     path('logout/',LogoutPage.as_view(), name='logout'),
]
