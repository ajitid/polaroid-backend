from django.urls import path
from knox import views as knox_views

from . import views

urlpatterns = [
    path("login", views.LoginView.as_view(), name="token_login"),
    path("logout", knox_views.LogoutView.as_view(), name="token_logout"),
    path("logoutall", knox_views.LogoutAllView.as_view(), name="token_logoutall"),
    path("user", views.user_info, name="user_info"),
]
