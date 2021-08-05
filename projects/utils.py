from .models import Project
from django.db.models import Q


def search_projects(request, search_query):
    projects = (
        Project.objects.distinct()
        .filter(
            Q(title__icontains=search_query)
            | Q(tags__name__icontains=search_query)
        )
        .order_by("created_at")
    )
    return projects
