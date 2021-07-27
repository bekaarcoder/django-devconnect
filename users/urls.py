from django.urls import path
from .views import profiles, user_profile


urlpatterns = [
    path("", profiles, name="profiles"),
    path("profile/<str:pk>/", user_profile, name="user-profile"),
]
