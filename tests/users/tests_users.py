import json
from typing import Callable

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase

from users.serializers import UserSerializer


class UserRegisterTests(APITestCase):

    register_url: str = reverse("register-user")

    def test_add_user(self):
        self.assertEqual(0, User.objects.count())
        resp = self.client.post(
            self.register_url, data={"username": "test", "password": "test"}
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
            self.register_url, data={"username": "test", "password": "test"}
        )
        test_resp = self.client.post(
            self.register_url, data={"username": "test", "password": "test"}
        )
        users_count = User.objects.count()
        self.assertEqual(test_resp.status_code, 400)
        self.assertEqual(users_count, 1)

    def test_incorrect_user_fields(self):
        resp = self.client.post(self.register_url, data={"username": "test2"})
        self.assertEqual(resp.status_code, 400)
        users_count = User.objects.count()
        self.assertEqual(users_count, 0)


class UserDeleteTests(APITestCase):

    register_url: str = reverse("register-user")

    def test_delete_user_success(self):
        self.client.post(
            self.register_url, data={"username": "test", "password": "test"}
        )
        resp = self.client.delete(reverse("delete-user", kwargs={"pk": 3}))
        self.assertEqual(resp.status_code, 200)
        users_count = User.objects.count()
        self.assertEqual(users_count, 0)

    def test_delete_if_user_not_exist(self):
        users_count = User.objects.count()
        self.assertEqual(users_count, 0)
        resp = self.client.delete(reverse("delete-user", kwargs={"pk": 2}))
        self.assertEqual(resp.status_code, 404)
        users_count = User.objects.count()
        self.assertEqual(users_count, 0)
