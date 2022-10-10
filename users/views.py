from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.utils import json_response, json_response_error
from users.serializers import UserSerializer


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


class UserDeleteView(APIView):
    """
    View для удаления пользователя
    """

    def delete(self, request: Request, pk: int = None):
        try:
            user = get_object_or_404(User, pk=pk)
        except Http404:
            return json_response_error(
                status=404, message=f"Пользователь с pk(id) {pk} не найден."
            )

        user.delete()
        serializer = UserSerializer(user)
        return json_response(
            status=200,
            data=serializer.data,
            message=f"Пользователь с pk(id) {pk} удален.",
        )
