from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


User = get_user_model()


class UserTests(APITestCase):

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

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

    def test_register_user(self):
        response = self.client.post(
            "/api/users/register/",
            {
                "username": "pedro",
                "email": "pedro@email.com",
                "password": "Senha12345",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        self.assertTrue(
            User.objects.filter(
                username="pedro"
            ).exists()
        )

    def test_get_my_profile(self):
        response = self.client.get(
            "/api/users/me/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["username"],
            "joao",
        )

    def test_update_my_profile(self):
        response = self.client.patch(
            "/api/users/me/",
            {
                "first_name": "Joao",
                "last_name": "Silva",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["first_name"],
            "Joao",
        )
        self.assertEqual(
            response.data["last_name"],
            "Silva",
        )

    def test_follow_user(self):
        response = self.client.post(
            f"/api/users/{self.other_user.id}/follow/"
        )

        self.assertEqual(response.status_code, 200)

        self.user.refresh_from_db()

        self.assertTrue(
            self.user.following.filter(
                id=self.other_user.id
            ).exists()
        )

    def test_following_list(self):
        self.user.following.add(
            self.other_user
        )

        response = self.client.get(
            "/api/users/following/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.data),
            1,
        )
        self.assertEqual(
            response.data[0]["username"],
            "maria",
        )