from django.urls import path

from .views import (
    ChangePasswordView,
    FollowersListView,
    FollowingListView,
    FollowView,
    MeView,
    RegisterView,
    UnfollowView,
)


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("me/", MeView.as_view(), name="me"),
    path(
        "change-password/",
        ChangePasswordView.as_view(),
        name="change-password",
    ),
    path(
        "<int:user_id>/follow/",
        FollowView.as_view(),
        name="follow",
    ),
    path(
        "<int:user_id>/unfollow/",
        UnfollowView.as_view(),
        name="unfollow",
    ),
    path(
        "following/",
        FollowingListView.as_view(),
        name="following",
    ),
    path(
        "followers/",
        FollowersListView.as_view(),
        name="followers",
    ),
]