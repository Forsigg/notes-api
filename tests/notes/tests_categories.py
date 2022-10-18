import json

from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from notes.models import Category, Note
from notes.serializers import CategorySerializer


class CategoryTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        author: User = User.objects.create_user(
            username="test",
            password="test",
            email="test@test.com",
        )
        cat = Category.objects.create(title="test category")
        Note.objects.create(
            text="Test", author=author, pub_date="2022-10-05", category=cat
        )
        cls.__user = author

    def setUp(self) -> None:
        resp = self.client.post(
            path="/api/token/",
            data={"username": self.__user.username, "password": "test"},
            format="json",
        )
        token = resp.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_success_create_category(self):
        cat_count = Category.objects.count()
        self.assertEqual(cat_count, 1)
        resp = self.client.post(
            "/api/v1/categories/", data={"title": "job"}, format="json"
        )
        self.assertEqual(resp.status_code, 201)
        cat_count = Category.objects.count()
        self.assertEqual(cat_count, 2)
        cat = Category.objects.get(pk=2)
        serializer = CategorySerializer(cat)
        self.assertEqual(cat.title, "job")
        json_body = json.loads(resp.content)["detail"]["data"]
        self.assertEqual(json_body, serializer.data)

    def test_success_get_category(self):
        resp = self.client.get("/api/v1/categories/1/")
        json_body = json.loads(resp.content)
        cat = Category.objects.get(pk=1)
        serializer = CategorySerializer(cat)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json_body["detail"]["data"], serializer.data)

    def test_success_get_list_categories(self):
        resp = self.client.get("/api/v1/categories/")
        self.assertEqual(resp.status_code, 200)
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        json_body = json.loads(resp.content)
        self.assertEqual(json_body["detail"]["data"], serializer.data)

    def test_success_delete_category(self):
        count_categories = Category.objects.count()
        self.assertEqual(1, count_categories)
        resp = self.client.delete("/api/v1/categories/1/")
        count_categories = Category.objects.count()
        self.assertEqual(0, count_categories)
