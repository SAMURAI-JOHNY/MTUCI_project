from django.conf.urls import static
from django.contrib import admin
from django.urls import path, include
from gameinfocus.views import UserAPIRegistr, UserView, LoginUserView, EmailVerify, LogoutUser
from lol.views import UserAPILol
from .yasg import urlpatterns as doc_patterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('lol/<str:course_name>/<int:block_id>', UserAPILol.as_view()),
    path('user', UserView.as_view()),
    path('registr', UserAPIRegistr.as_view()),
    path('login', LoginUserView.as_view()),
    path('logout/', LogoutUser.as_view()),
    path('verify', EmailVerify.as_view()),
]

urlpatterns += doc_patterns
