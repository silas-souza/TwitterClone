from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Comment, Post
from .serializers import CommentSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        return Post.objects.filter(
            author__in=[user, *user.following.all()]
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        post = self.get_object()

        if post.likes.filter(id=request.user.id).exists():
            return Response(
                {"message": "Você já curtiu esta postagem."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        post.likes.add(request.user)

        return Response(
            {"message": "Postagem curtida com sucesso."},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["delete"])
    def unlike(self, request, pk=None):
        post = self.get_object()

        if not post.likes.filter(id=request.user.id).exists():
            return Response(
                {"message": "Você não curtiu esta postagem."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        post.likes.remove(request.user)

        return Response(
            {"message": "Curtida removida com sucesso."},
            status=status.HTTP_200_OK,
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_id")

        serializer.save(
            author=self.request.user,
            post_id=post_id,
        )