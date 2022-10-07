from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class LoginView(APIView):
    def post(self, request: Request) -> Response:
        # TODO: Сделать вью для логина пользователя
        pass
