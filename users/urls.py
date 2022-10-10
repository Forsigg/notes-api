from django.urls import path
from users.views import UserRegisterView, UserDeleteView

# URL: /api/v1/auth/...
urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register-user"),
    path("users/<int:pk>/", UserDeleteView.as_view(), name='delete-user'),
]
