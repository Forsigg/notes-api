import json
from typing import Optional
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

import notes
from notes.models import Note
from notes.serializers import NoteSerializer


class NoteTests(APITestCase):
    __user: Optional[User] = None
    __headers = None

    @classmethod
    def setUpTestData(cls):
        author: User = User.objects.create_user(
            username="test",
            password="test",
            email="test@test.com",
        )
        Note.objects.create(text="Test", author=author, pub_date="2022-10-05")
        Note.objects.create(text="Test2", author=author, pub_date="2022-10-05")
        cls.__user = author

    def setUp(self) -> None:
        resp = self.client.post(
            path="/api/token/",
            data={"username": self.__user.username, "password": "test"},
            format="json",
        )
        token = resp.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_success_get_in_view(self):
        resp = self.client.get("/api/v1/notes/1/")
        note = Note.objects.get(pk=1)
        serializer = NoteSerializer(note)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.content)["detail"]["data"], serializer.data)

    def test_success_create_in_view(self):
        resp = self.client.post(
            "/api/v1/notes/",
            data={"text": "test in view", "author": 1},
            format="json",
        )
        self.assertEqual(resp.status_code, 200)
        note = Note.objects.get(pk=3)
        self.assertEqual(note.text, "test in view")

    def test_success_get_list_notes(self):
        resp = self.client.get("/api/v1/notes/")
        notes = Note.objects.all()
        serializer = NoteSerializer(notes, many=True)
        self.assertEqual(json.loads(resp.content)["detail"]["data"], serializer.data)

    def test_success_delete_note(self):
        self.client.delete("/api/v1/notes/2/")
        count = Note.objects.all().count()
        self.assertRaises(notes.models.Note.DoesNotExist, Note.objects.get, pk=2)
        self.assertEqual(1, count)
