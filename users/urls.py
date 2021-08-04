from django.urls import path
from .views import (
    profiles,
    user_profile,
    login_user,
    logout_user,
    register_user,
    user_account,
    edit_account,
    create_skill,
    update_skill,
    delete_skill,
)


urlpatterns = [
    path("", profiles, name="profiles"),
    path("profile/<str:pk>/", user_profile, name="user-profile"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("register/", register_user, name="register"),
    path("account/", user_account, name="account"),
    path("edit-account/", edit_account, name="edit-account"),
    path("create-skill/", create_skill, name="create-skill"),
    path("update-skill/<str:pk>/", update_skill, name="update-skill"),
    path("delete-skill/<str:pk>/", delete_skill, name="delete-skill"),
]
