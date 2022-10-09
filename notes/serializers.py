from rest_framework import serializers

from notes.models import Note, Category


class NoteSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для модели заметки (Note)
    """

    class Meta:
        model = Note
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериалайзер для модели категории (Category)
    """

    class Meta:
        model = Category
        fields = "__all__"
