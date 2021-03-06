"""donate_hub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
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
from django.contrib import admin
from django.urls import path
import donating.views as donating_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', donating_views.LandingPageView.as_view(), name='index'),
    path('donate/', donating_views.AddDonationView.as_view(), name='donation'),
    path('success/', donating_views.SuccessView.as_view(), name='success'),
    path('login/', donating_views.LoginView.as_view(), name='login'),
    path('logout/', donating_views.LogoutView.as_view(), name='logout'),
    path('register/', donating_views.RegisterView.as_view(), name='register'),
    path('user-profile/', donating_views.UserView.as_view(), name='profile'),
    path('upload/', donating_views.Donation2View.as_view(), name='upload'),
]
