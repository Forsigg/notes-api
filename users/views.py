from django.shortcuts import redirect
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.utils import json_response, json_response_error
from users.serializers import UserSerializer, UserLoginSerializer


class LoginView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserLoginSerializer(request.data)
        if serializer.is_valid():
            request.headers['Authorization'] = f'Bearer ' \
                                               f'{serializer.validated_data["token"]}'
            return json_response(status=200, data={serializer.validated_data},
                                 message='Пользователь залогинен')
        else:
            return json_response_error(status=400, data=serializer.errors)
