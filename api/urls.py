from django.urls import path
from . import views


urlpatterns = [
    path("", views.get_routes),
    path("projects/", views.get_projects),
    path("projects/<str:pk>", views.get_project),
]
