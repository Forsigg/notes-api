from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from notes.models import Note
from notes.serializers import NoteSerializer


class NoteViewSet(viewsets.ViewSet):
    """
    ViewSet для добавления, обновления, удаления, получения данных о заметке
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request: Request) -> Response:
        """
        Вью для добавления заметки в БД
        URL: /api/v1/notes/
        """
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def retrieve(self, request: Request, pk: int = None) -> Response:
        """
        Вью для получения заметки по id(pk)
        URL: /api/v1/notes/<pk>
        """
        queryset = Note.objects.all()
        note = get_object_or_404(queryset, pk=pk)
        serializer = NoteSerializer(note)
        return Response(serializer.data)

    def list(self, request: Request) -> Response:
        """
        Вью для получения всех заметок, имеющихся в БД
        URL: /api/v1/notes/
        """
        queryset = Note.objects.all()
        serializer = NoteSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def list_by_user_id(self, request: Request, user_pk: int = None) -> Response:
        """
        Вью для получения списка заметок по id пользователя. Принимает обязательный
        параметр user_pk: int
        URL: /api/v1/notes/users/<user_pk>
        """
        notes = Note.objects.all().filter(author=user_pk)
        if notes:
            serializer = NoteSerializer(notes, many=True)
            return Response(serializer.data)
        else:
            return Response(
                data={
                    "detail": {"error": f"Пользователь с user_pk {user_pk} не найден"}
                }
            )

    def destroy(self, request: Request, pk: int = None):
        note = Note.objects.get(pk=pk)
        if note:
            note.delete()
            return Response(data={
                'status': 'ok',
                'message': f'Заметка с id(pk) {pk} удалена'
            })
        else:
            return Response(data={
                    "detail": {"error": f"Заметка с id(pk) {pk} не найдена"}
                })
