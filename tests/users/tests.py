import json

from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from users.serializers import UserSerializer


class UserTests(APITestCase):
    def test_add_user(self):
        self.assertEqual(0, User.objects.count())
        resp = self.client.post(
            "/api/v1/auth/register/", data={"username": "test", "password": "test"}
        )
        json_resp = json.loads(resp.content)["detail"]["data"]
        self.assertEqual(resp.status_code, 201)
        user = User.objects.get(username="test")
        serializer = UserSerializer(user)
        self.assertEqual(
            json_resp,
            {"id": serializer.data["id"], "username": serializer.data["username"]},
        )
