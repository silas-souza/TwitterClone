from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, PostViewSet


router = DefaultRouter()
router.register("", PostViewSet, basename="post")


comment_list = CommentViewSet.as_view({
    "get": "list",
    "post": "create",
})

comment_detail = CommentViewSet.as_view({
    "get": "retrieve",
    "delete": "destroy",
})


urlpatterns = [
    path("", include(router.urls)),

    path(
        "<int:post_id>/comments/",
        comment_list,
        name="comment-list",
    ),

    path(
        "<int:post_id>/comments/<int:pk>/",
        comment_detail,
        name="comment-detail",
    ),
]