from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("cadastro/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("postar/", views.create_post, name="create_post"),
    path(
        "post/<int:post_id>/curtir/",
        views.like_post,
        name="like_post",
    ),
    path(
        "post/<int:post_id>/comentar/",
        views.add_comment,
        name="add_comment",
    ),
    path(
        "seguir/<int:user_id>/",
        views.follow_user,
        name="follow_user",
    ),
    path(
        "deixar-de-seguir/<int:user_id>/",
        views.unfollow_user,
        name="unfollow_user",
    ),
    path("perfil/<int:user_id>/", views.user_profile, name="user_profile"),
    path("perfil/", views.profile, name="profile"),
]