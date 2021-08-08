from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from .utils import search_projects


def projects(request):
    search_query = ""

    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    projects = search_projects(request, search_query)

    page = 1
    if request.GET.get("page"):
        page = request.GET.get("page")
    results = 3
    paginator = Paginator(projects, results)

    projects = paginator.page(page)

    context = {"projects": projects, "search_query": search_query}
    return render(request, "projects/projects.html", context)


def project(request, pk):
    form = ReviewForm()
    project = Project.objects.get(id=pk)
    tags = project.tags.all()
    reviews = project.review_set.all()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.owner = request.user.profile
            review.project = project
            review.save()
            project.update_vote_count
            messages.success(request, "Review added successfully!")
            return redirect("single-project", pk=project.id)

    context = {
        "project": project,
        "tags": tags,
        "reviews": reviews,
        "form": form,
    }
    return render(request, "projects/single-project.html", context)


@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect("projects")

    context = {"form": form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def updateProject(request, pk):
    profile = request.user.profile
    try:
        project = profile.project_set.get(id=pk)
    except:
        return redirect("projects")

    form = ProjectForm(instance=project)

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect("projects")

    context = {"form": form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile
    try:
        project = profile.project_set.get(id=pk)
    except:
        return redirect("projects")

    if request.method == "POST":
        project.delete()
        return redirect("projects")

    context = {"project": project}
    return render(request, "projects/delete_project.html", context)


# @login_required(login_url="login")
# def add_review(request, pk):
#     profile = request.user.profile
#     form = ReviewForm()

#     context = {"form": form}
#     return render(request, )
