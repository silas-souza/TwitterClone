from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render

from posts.models import Comment, Post


User = get_user_model()


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            login(request, user)
            return redirect("home")

        return render(
            request,
            "accounts/login.html",
            {"error": "Usuário ou senha inválidos."},
        )

    return render(request, "accounts/login.html")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not username or not password:
            return render(
                request,
                "accounts/register.html",
                {"error": "Usuário e senha são obrigatórios."},
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "accounts/register.html",
                {"error": "Esse usuário já existe."},
            )

        if len(password) < 8:
            return render(
                request,
                "accounts/register.html",
                {"error": "A senha deve ter pelo menos 8 caracteres."},
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        login(request, user)
        return redirect("home")

    return render(request, "accounts/register.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def home(request):
    following = request.user.following.all()

    posts = (
        Post.objects.filter(
            author__in=[request.user, *following]
        )
        .select_related("author")
        .prefetch_related("likes", "comments__author")
        .order_by("-created_at")
    )

    users = User.objects.exclude(id=request.user.id).order_by("username")

    return render(
        request,
        "posts/home.html",
        {
            "posts": posts,
            "users": users,
        },
    )


@login_required
def create_post(request):
    if request.method == "POST":
        content = request.POST.get("content", "").strip()

        if content:
            Post.objects.create(
                author=request.user,
                content=content,
            )

    return redirect("home")


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect("home")


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        content = request.POST.get("content", "").strip()

        if content:
            Comment.objects.create(
                post=post,
                author=request.user,
                content=content,
            )

    return redirect("home")


@login_required
def follow_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if user != request.user:
        request.user.following.add(user)

    return redirect("home")


@login_required
def unfollow_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    request.user.following.remove(user)

    return redirect("home")


@login_required
def profile(request):
    user = request.user

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()

        if username:
            existing = User.objects.filter(
                username=username
            ).exclude(id=user.id).exists()

            if not existing:
                user.username = username

        user.email = email

        if request.FILES.get("profile_picture"):
            user.profile_picture = request.FILES["profile_picture"]

        user.save()

        return redirect("profile")

    posts = (
        Post.objects
        .filter(author=user)
        .select_related("author")
        .prefetch_related("likes", "comments__author")
        .order_by("-created_at")
    )

    return render(
        request,
        "accounts/profile.html",
        {
            "profile_user": user,
            "posts": posts,
            "followers_count": user.followers.count(),
            "following_count": user.following.count(),
        },
    )

@login_required
def user_profile(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)

    posts = (
        Post.objects
        .filter(author=profile_user)
        .select_related("author")
        .prefetch_related("likes", "comments__author")
        .order_by("-created_at")
    )

    return render(
        request,
        "accounts/user_profile.html",
        {
            "profile_user": profile_user,
            "posts": posts,
            "followers_count": profile_user.followers.count(),
            "following_count": profile_user.following.count(),
            "is_following": request.user.following.filter(
                id=profile_user.id
            ).exists(),
        },
    )