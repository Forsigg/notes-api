import jwt
from django.contrib.auth.models import User, update_last_login
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.settings import api_settings

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        exclude = ['password']


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, min_length=5, required=True)
    password = serializers.CharField(min_length=5, max_length=30, required=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data: dict) -> dict:
        username = data.get('username', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                'Пользователь с таким именем и паролем не найден'
            )

        try:
            # token = jwt.encode(
            #     'id': user.id
            # )
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'Пользователь с таким именем и паролем не существует'
            )
        return {
            'email': user.email,
            'token': jwt_token
        }


