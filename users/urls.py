from django.urls import path
from users.views import LoginView, UserRegisterView


# URL: /api/v1/auth/...
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
]
