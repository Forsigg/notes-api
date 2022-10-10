from django.urls import path
from users.views import UserRegisterView


# URL: /api/v1/auth/...
urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
]
