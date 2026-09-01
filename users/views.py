from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProfileSerializer, RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework.generics import get_object_or_404

from .serializers import RegisterSerializer


class RegisterView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            return Response(
                {
                    "message": "Usuário criado com sucesso.",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                    },
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(
            request.user,
            context={"request": request},
        )

        return Response(serializer.data)

    def patch(self, request):
        serializer = ProfileSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={"request": request},
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")

        if not current_password or not new_password:
            return Response(
                {
                    "detail": "current_password e new_password são obrigatórios."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not request.user.check_password(current_password):
            return Response(
                {"detail": "Senha atual incorreta."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(new_password) < 8:
            return Response(
                {"detail": "A nova senha deve ter pelo menos 8 caracteres."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.user.set_password(new_password)
        request.user.save()

        return Response(
            {"message": "Senha alterada com sucesso."},
            status=status.HTTP_200_OK,
        )
User = get_user_model()


class FollowView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(User, id=user_id)

        if user_to_follow == request.user:
            return Response(
                {"detail": "Você não pode seguir a si mesmo."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.user.following.add(user_to_follow)

        return Response(
            {"message": f"Agora você segue {user_to_follow.username}."},
            status=status.HTTP_200_OK,
        )


class UnfollowView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id):
        user_to_unfollow = get_object_or_404(User, id=user_id)

        request.user.following.remove(user_to_unfollow)

        return Response(
            {"message": f"Você deixou de seguir {user_to_unfollow.username}."},
            status=status.HTTP_200_OK,
        )
class FollowingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = request.user.following.all()

        return Response(
            [
                {
                    "id": user.id,
                    "username": user.username,
                }
                for user in users
            ]
        )


class FollowersListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = request.user.followers.all()

        return Response(
            [
                {
                    "id": user.id,
                    "username": user.username,
                }
                for user in users
            ]
        )