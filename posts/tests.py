from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Comment, Post


User = get_user_model()


class PostTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="joao",
            email="joao@email.com",
            password="Senha12345",
        )

        self.other_user = User.objects.create_user(
            username="maria",
            email="maria@email.com",
            password="Senha12345",
        )

        self.token = Token.objects.create(
            user=self.user
        )

        self.user.following.add(
            self.other_user
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

    def test_create_post(self):
        response = self.client.post(
            "/api/posts/",
            {
                "content": "Minha postagem de teste",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data["author"],
            self.user.id,
        )
        self.assertEqual(
            response.data["content"],
            "Minha postagem de teste",
        )

    def test_list_posts(self):
        Post.objects.create(
            author=self.user,
            content="Postagem do João",
        )

        response = self.client.get(
            "/api/posts/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_like_post(self):
        post = Post.objects.create(
            author=self.other_user,
            content="Postagem da Maria",
        )

        response = self.client.post(
            f"/api/posts/{post.id}/like/"
        )

        self.assertEqual(response.status_code, 200)

        post.refresh_from_db()

        self.assertTrue(
            post.likes.filter(
                id=self.user.id
            ).exists()
        )

    def test_unlike_post(self):
        post = Post.objects.create(
            author=self.other_user,
            content="Postagem da Maria",
        )

        post.likes.add(
            self.user
        )

        response = self.client.delete(
            f"/api/posts/{post.id}/unlike/"
        )

        self.assertEqual(response.status_code, 200)

        post.refresh_from_db()

        self.assertFalse(
            post.likes.filter(
                id=self.user.id
            ).exists()
        )

    def test_create_comment(self):
        post = Post.objects.create(
            author=self.other_user,
            content="Postagem da Maria",
        )

        response = self.client.post(
            f"/api/posts/{post.id}/comments/",
            {
                "content": "Excelente postagem!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data["post"],
            post.id,
        )
        self.assertEqual(
            response.data["author"],
            self.user.id,
        )

    def test_list_comments(self):
        post = Post.objects.create(
            author=self.other_user,
            content="Postagem da Maria",
        )

        Comment.objects.create(
            post=post,
            author=self.user,
            content="Muito bom!",
        )

        response = self.client.get(
            f"/api/posts/{post.id}/comments/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_delete_comment(self):
        post = Post.objects.create(
            author=self.other_user,
            content="Postagem da Maria",
        )

        comment = Comment.objects.create(
            post=post,
            author=self.user,
            content="Comentário para excluir",
        )

        response = self.client.delete(
            f"/api/posts/{post.id}/comments/{comment.id}/"
        )

        self.assertEqual(response.status_code, 204)

        self.assertFalse(
            Comment.objects.filter(
                id=comment.id
            ).exists()
        )