from django.urls import path
from rest_framework import routers
from notes.views import NoteViewSet, CategoryViewSet

router = routers.SimpleRouter()
router.register(r"notes", NoteViewSet, basename="notes")  # URL: /api/v1/notes
router.register(r'categories', CategoryViewSet, basename='categories') # URL:
# /api/v1/categories


# URL: /api/v1/...
urlpatterns = [
    path("notes/users/<int:user_pk>/", NoteViewSet.as_view({"get": "list_by_user_id"}))
]

urlpatterns += router.urls
