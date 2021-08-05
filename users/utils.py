from django.db.models import Q
from .models import Profile, Skill


def search_profiles(request, search_query):
    skills = Skill.objects.filter(name__icontains=search_query)
    profiles = (
        Profile.objects.distinct()
        .filter(
            Q(name__icontains=search_query)
            | Q(short_bio__icontains=search_query)
            | Q(skill__in=skills)
        )
        .order_by("created_at")
    )
    return profiles
