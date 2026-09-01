from django.contrib import messages
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
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

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
            {
                "error": "Usuário ou senha inválidos.",
            },
        )

    return render(request, "accounts/login.html")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        if not username or not password:
            return render(
                request,
                "accounts/register.html",
                {
                    "error": "Usuário e senha são obrigatórios.",
                },
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "accounts/register.html",
                {
                    "error": "Esse usuário já existe.",
                },
            )

        if len(password) < 8:
            return render(
                request,
                "accounts/register.html",
                {
                    "error": "A senha deve ter pelo menos 8 caracteres.",
                },
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
    # =========================================================
    # FEED
    # =========================================================
    # O feed mostra somente publicações das pessoas que
    # o usuário atual segue.
    #
    # A própria publicação NÃO aparece no feed.
    # =========================================================

    following = request.user.following.all()

    posts = (
        Post.objects
        .filter(author__in=following)
        .select_related("author")
        .prefetch_related(
            "likes",
            "comments__author",
        )
        .order_by("-created_at")
    )

    # Lista de usuários para seguir.
    users = (
        User.objects
        .exclude(id=request.user.id)
        .order_by("username")
    )

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
    post = get_object_or_404(
        Post,
        id=post_id,
    )

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect("home")


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
    )

    if request.method == "POST":
        content = request.POST.get(
            "content",
            "",
        ).strip()

        if content:
            Comment.objects.create(
                post=post,
                author=request.user,
                content=content,
            )

    return redirect("home")


@login_required
def follow_user(request, user_id):
    user = get_object_or_404(
        User,
        id=user_id,
    )

    if user != request.user:
        request.user.following.add(user)

    return redirect("home")


@login_required
def unfollow_user(request, user_id):
    user = get_object_or_404(
        User,
        id=user_id,
    )

    request.user.following.remove(user)

    return redirect("home")


@login_required
def profile(request):
    user = request.user

    if request.method == "POST":

        # =====================================================
        # NOME DE USUÁRIO
        # =====================================================

        username = request.POST.get(
            "username",
            "",
        ).strip()

        # Só altera se o campo tiver sido preenchido.
        if username:

            if User.objects.filter(
                username=username
            ).exclude(
                pk=user.pk
            ).exists():

                messages.error(
                    request,
                    "Esse nome de usuário já está sendo usado.",
                )

                return redirect("profile")

            user.username = username

        # =====================================================
        # NOME
        # =====================================================

        first_name = request.POST.get(
            "first_name",
            "",
        ).strip()

        # Só altera se o campo tiver sido preenchido.
        if first_name:
            user.first_name = first_name

        # =====================================================
        # E-MAIL
        # =====================================================

        email = request.POST.get(
            "email",
            "",
        ).strip()

        # Só altera se o campo tiver sido preenchido.
        if email:
            user.email = email

        # =====================================================
        # FOTO DE PERFIL
        # =====================================================

        profile_picture = request.FILES.get(
            "profile_picture",
        )

        if profile_picture:
            user.profile_picture = profile_picture

        # =====================================================
        # SENHA
        # =====================================================

        current_password = request.POST.get(
            "current_password",
            "",
        )

        new_password = request.POST.get(
            "new_password",
            "",
        )

        new_password_confirm = request.POST.get(
            "new_password_confirm",
            "",
        )

        senha_alterada = False

        # Só entra na alteração de senha se algum campo
        # de senha tiver sido preenchido.
        if (
            current_password
            or new_password
            or new_password_confirm
        ):

            if not current_password:
                messages.error(
                    request,
                    "Digite sua senha atual para alterar a senha.",
                )

                return redirect("profile")

            if not user.check_password(
                current_password
            ):
                messages.error(
                    request,
                    "A senha atual está incorreta.",
                )

                return redirect("profile")

            if not new_password:
                messages.error(
                    request,
                    "Digite a nova senha.",
                )

                return redirect("profile")

            if len(new_password) < 8:
                messages.error(
                    request,
                    "A nova senha deve ter pelo menos 8 caracteres.",
                )

                return redirect("profile")

            if new_password != new_password_confirm:
                messages.error(
                    request,
                    "As novas senhas não são iguais.",
                )

                return redirect("profile")

            user.set_password(new_password)

            senha_alterada = True

        # =====================================================
        # SALVAR
        # =====================================================

        user.save()

        # Mantém o usuário conectado depois de trocar a senha.
        if senha_alterada:
            login(request, user)

        messages.success(
            request,
            "Perfil atualizado com sucesso!",
        )

        return redirect("profile")

    # =========================================================
    # PUBLICAÇÕES DO PRÓPRIO PERFIL
    # =========================================================

    posts = (
        Post.objects
        .filter(author=user)
        .select_related("author")
        .prefetch_related(
            "likes",
            "comments__author",
        )
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
    profile_user = get_object_or_404(
        User,
        id=user_id,
    )

    posts = (
        Post.objects
        .filter(author=profile_user)
        .select_related("author")
        .prefetch_related(
            "likes",
            "comments__author",
        )
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
                id=profile_user.id,
            ).exists(),
        },
    )