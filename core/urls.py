from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from django.urls import path
from .views import UserSignupView, UserLoginView

urlpatterns = [
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("signup/", UserSignupView.as_view(), name="user_signup"),
]
