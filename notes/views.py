from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.utils import json_response_error, json_response
from notes.models import Note, Category
from notes.serializers import NoteSerializer, CategorySerializer


class NoteViewSet(viewsets.ViewSet):
    """
    ViewSet для добавления, обновления, удаления, получения данных о заметке
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request: Request) -> Response:
        """
        Method POST
        Вью для добавления заметки в БД
        URL: /api/v1/notes/
        """
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return json_response(
                data=serializer.data, message="Заметка успешно " "создана.", status=201
            )

        return json_response_error(
            status=400, data=serializer.errors, message="Ошибка в данных запроса"
        )

    def retrieve(self, request: Request, pk: int = None) -> Response:
        """
        Method GET
        Вью для получения заметки по id(pk)
        URL: /api/v1/notes/<pk>
        """
        try:
            note = get_object_or_404(Note, pk=pk)
        except Http404:
            return json_response_error(
                status=404, message=f"Заметка с pk(id) {pk} не найдена."
            )
        serializer = NoteSerializer(note)
        return json_response(data=serializer.data)

    def list(self, request: Request) -> Response:
        """
        Method GET
        Вью для получения всех заметок, имеющихся в БД
        URL: /api/v1/notes/
        """
        queryset = Note.objects.all()
        serializer = NoteSerializer(queryset, many=True)
        return json_response(data=serializer.data)

    @action(detail=False, methods=["get"])
    def list_by_user_id(self, request: Request, user_pk: int = None) -> Response:
        """
        Method get
        Вью для получения списка заметок по id пользователя. Принимает обязательный
        параметр user_pk: int
        URL: /api/v1/notes/users/<user_pk>
        """
        notes = Note.objects.all().filter(author=user_pk)
        if notes:
            serializer = NoteSerializer(notes, many=True)
            return json_response(data=serializer.data)
        else:
            return json_response_error(
                status=404, message=f"Пользователь с user_pk {user_pk} не найден."
            )

    def destroy(self, request: Request, pk: int = None):
        """
        Method DELETE
        Вью для удаления заметки. Принимает помимо объекта Request также pk (id) заметки
        URL: /api/v1/notes/<pk:int>
        """
        try:
            note = get_object_or_404(Note, pk=pk)
        except Http404:
            return json_response_error(
                status=404, message=f"Заметка с pk(id) {pk} не найдена."
            )
        note.delete()
        serializer = NoteSerializer(note)
        return json_response(
            status=200, message=f"Заметка с id(pk) {pk} удалена", data=serializer.data
        )

    def update(self, request: Request, pk: int = None) -> Response:
        try:
            note = get_object_or_404(Note, pk=pk)
        except Http404:
            return json_response_error(
                status=404, message=f"Заметка с pk(id) {pk} не найдена."
            )
        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return json_response(
                status=201,
                message=f"Заметка с pk(id) {pk} " f"обновлена.",
                data=serializer.data,
            )
        else:
            return json_response_error(
                status=400, data=serializer.errors, message="error"
            )

    def partial_update(self, request: Request, pk: int = None) -> Response:
        # TODO: Доделать частичное обновление заметки
        pass


class CategoryViewSet(viewsets.ViewSet):
    """
    ViewSet для добавления, удаления, изменения и получения категории, а также списка
    категорий
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def retrieve(self, request: Request, pk: int = None) -> Response:
        """
        Method GET
        View для получения категории по её id(pk)
        URL: /api/v1/categories/<int:pk>/
        """
        try:
            category = get_object_or_404(Category, pk=pk)
        except Http404:
            return json_response_error(
                status=404, message=f"Категория с pk(id) {pk} не найдена"
            )
        serializer = CategorySerializer(category)
        return json_response(status=200, data=serializer.data)

    def create(self, request: Request) -> Response:
        """
        Method POST
        View для добавления категории в БД
        URL: /api/v1/categories/
        """
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return json_response(
                status=201, data=serializer.data, message=f"Категория успешно создана"
            )

        return json_response_error(
            status=400,
            data=serializer.errors,
            message="Ошибка " "в " "данных " "запроса",
        )

    def list(self, request: Request) -> Response:
        """
        Method GET
        View для получения всех категорий, имеющихся в БД
        URL: /api/v1/categories/
        """
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return json_response(data=serializer.data)

    def destroy(self, request: Request, pk: int = None) -> Response:
        try:
            category = get_object_or_404(Category, pk=pk)
        except Http404:
            return json_response_error(status=404, message=f"Категория с pk(id) {pk} не найдена")

        category.delete()
        serializer = CategorySerializer(category)
        return json_response(status=204, message=f"Категория с pk(id) {pk} успешно "
                                                 f"удалена")


