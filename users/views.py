from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.utils import json_response, json_response_error
from users.serializers import UserSerializer


class LoginView(APIView):
    def post(self, request: Request) -> Response:
        # TODO: Сделать вью для логина пользователя
        pass


class UserRegisterView(APIView):
    """
    View для добавления (регистрации) пользователя
    """

    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"],
            )
            return json_response(
                status=201,
                message=f"Пользователь с pk(id) {user.id} " f"создан",
                data={"id": user.id, "username": user.username},
            )
        else:
            return json_response_error(status=400, data=serializer.errors)
