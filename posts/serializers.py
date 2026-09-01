from rest_framework import serializers

from .models import Comment, Post


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(
        source="author.username",
        read_only=True,
    )

    likes_count = serializers.IntegerField(
        source="likes.count",
        read_only=True,
    )

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "author_username",
            "content",
            "likes_count",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "author",
            "author_username",
            "likes_count",
            "created_at",
            "updated_at",
        )


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    author_username = serializers.CharField(
        source="author.username",
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = (
            "id",
            "post",
            "author",
            "author_username",
            "content",
            "created_at",
        )

        read_only_fields = (
            "post",
            "author",
            "author_username",
            "created_at",
        )