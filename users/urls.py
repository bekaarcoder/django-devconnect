from django.urls import path
from .views import (
    profiles,
    user_profile,
    login_user,
    logout_user,
    register_user,
    user_account,
)


urlpatterns = [
    path("", profiles, name="profiles"),
    path("profile/<str:pk>/", user_profile, name="user-profile"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("register/", register_user, name="register"),
    path("account/", user_account, name="account"),
]
