from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .utils import search_profiles


def login_user(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect("profiles")

    if request.method == "POST":
        username = request.POST["username"].lower()
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username does not exist.")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(
                request.GET["next"] if "next" in request.GET else "account"
            )
        else:
            messages.error(request, "Username/Password is incorrect")

    context = {"page": page}

    return render(request, "users/login_register.html", context)


def logout_user(request):
    logout(request)
    messages.info(request, "User logged out successfully!")
    return redirect("login")


def register_user(request):
    page = "register"
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            # messages.success(request, "User account created successfully!")

            login(request, user)
            return redirect("edit-account")
        else:
            messages.error(
                request, "An error has occurred during registration!"
            )

    context = {"page": page, "form": form}

    return render(request, "users/login_register.html", context)


def profiles(request):
    search_query = ""

    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    profiles = search_profiles(request, search_query)

    page = 1
    if request.GET.get("page"):
        page = request.GET.get("page")
    results = 9
    paginator = Paginator(profiles, results)

    profiles = paginator.page(page)

    context = {"profiles": profiles, "search_query": search_query}
    return render(request, "users/profiles.html", context)


def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    top_skills = []
    other_skills = []
    all_skills = profile.skill_set.all()
    for skill in all_skills:
        if skill.description == "":
            other_skills.append(skill)
        else:
            top_skills.append(skill)
    # top_skills = profile.skill_set.exclude(description__exact="")
    # other_skills = profile.skill_set.filter(description="")
    context = {
        "profile": profile,
        "top_skills": top_skills,
        "other_skills": other_skills,
    }
    return render(request, "users/user-profile.html", context)


@login_required(login_url="login")
def user_account(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    context = {"profile": profile, "skills": skills}
    return render(request, "users/account.html", context)


@login_required(login_url="login")
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect("account")
    context = {"form": form}
    return render(request, "users/profile_form.html", context)


@login_required(login_url="login")
def create_skill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, "Skill added successfully!")
            return redirect("account")

    context = {"form": form}
    return render(request, "users/skill_form.html", context)


@login_required(login_url="login")
def update_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill updated successfully!")
            return redirect("account")

    context = {"form": form}
    return render(request, "users/skill_form.html", context)


@login_required(login_url="login")
def delete_skill(request, pk):
    profile = request.user.profile
    try:
        skill = profile.skill_set.get(id=pk)
    except:
        return redirect("account")

    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill deleted successfully!")
        return redirect("account")

    context = {"skill": skill}
    return render(request, "users/delete_skill.html", context)


@login_required(login_url="login")
def inbox(request):
    profile = request.user.profile
    message_requests = (
        profile.messages.all()
    )  # using the related_name='messages' defined in the model
    unread_messages = message_requests.filter(is_read=False).count()
    context = {"message_requests": message_requests, "unread": unread_messages}
    return render(request, "users/inbox.html", context)


@login_required(login_url="login")
def view_message(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {"message": message}
    return render(request, "users/message.html", context)


def send_message(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email

            message.save()
            messages.success(request, "Message sent succefully!")
            return redirect("user-profile", pk=recipient.id)

    context = {"form": form, "recipient": recipient}
    return render(request, "users/message_form.html", context)
