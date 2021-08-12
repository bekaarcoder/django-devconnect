from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import ProjectSerializer
from projects.models import Project, Review


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username
        token["message"] = "Hello World!"

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(["GET"])
def get_routes(request):
    routes = [
        {"GET": "api/projects"},
        {"GET": "api/projects/id"},
        {"POST": "api/projects/id/vote"},
        {"POST": "api/users/token"},
        {"POST": "api/users/token/refresh"},
    ]
    return Response(routes)


@api_view(["GET"])
def get_projects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_project(request, pk):
    projects = Project.objects.get(id=pk)
    serializer = ProjectSerializer(projects, many=False)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def project_vote(request, pk):
    project = Project.objects.get(id=pk)
    user = request.user.profile
    data = request.data  # Get the request body

    review, created = Review.objects.get_or_create(
        owner=user,
        project=project,
    )

    review.value = data["value"]
    review.save()
    project.update_vote_count

    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)
