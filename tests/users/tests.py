import json

from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from users.serializers import UserSerializer


class UserRegisterTests(APITestCase):
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

    def test_user_already_exist(self):
        self.client.post(
            "/api/v1/auth/register/", data={"username": "test", "password": "test"}
        )
        test_resp = self.client.post(
            "/api/v1/auth/register/", data={"username": "test", "password": "test"}
        )
        users_count = User.objects.count()
        self.assertEqual(test_resp.status_code, 400)
        self.assertEqual(users_count, 1)

    def test_incorrect_user_fields(self):
        resp = self.client.post("/api/v1/auth/register/", data={"username": "test2"})
        self.assertEqual(resp.status_code, 400)
        users_count = User.objects.count()
        self.assertEqual(users_count, 0)


class UserDeleteTests(APITestCase):
    def test_delete_user_success(self):
        self.client.post(
            "/api/v1/auth/register/", data={"username": "test", "password": "test"}
        )
        resp = self.client.delete("/api/v1/auth/users/1/")
        self.assertEqual(resp.status_code, 200)
        users_count = User.objects.count()
        self.assertEqual(users_count, 0)

    def test_delete_if_user_not_exist(self):
        users_count = User.objects.count()
        self.assertEqual(users_count, 0)
        resp = self.client.delete("/api/v1/auth/users/1/")
        self.assertEqual(resp.status_code, 404)
        users_count = User.objects.count()
        self.assertEqual(users_count, 0)
