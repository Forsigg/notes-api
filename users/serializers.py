from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для модели пользователя (User)
    """

    class Meta:
        model = User
        fields = "__all__"
