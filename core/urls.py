from django.urls import path
from .views import (
    UserSignupView,
    UserLoginView,
    CookieTokenRefreshView,
    LogoutView,
    LogoutAllView,
)

urlpatterns = [
    path("refresh/", CookieTokenRefreshView.as_view(), name="token_refresh"),
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("signup/", UserSignupView.as_view(), name="user_signup"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("logout-all/", LogoutAllView.as_view(), name="logout-all"),
]
