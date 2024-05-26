"""
URL configuration for Game_in_focus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf.urls import static
from django.contrib import admin
from django.urls import path, include
from gameinfocus.views import UserAPIRegistr, UserView, LoginUserView, EmailVerify, LogoutUser
from lol.views import UserAPILol
from gameinfocus.models import User
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('lol/<str:course_name>/<int:block_id>', UserAPILol.as_view()),
    path('user/', UserView.as_view()),
    path('registr/', UserAPIRegistr.as_view()),
    path('login/', LoginUserView.as_view()),
    path('logout/', LogoutUser.as_view()),
    path('mail/', EmailVerify.as_view()),
]

