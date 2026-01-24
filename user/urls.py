from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from user.views import CreateUserView, ManageUserView, LogoutView, RegisterTelegramView

urlpatterns = [
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", CreateUserView.as_view(), name="register"),
    path("telegram/connect/", RegisterTelegramView.as_view(), name="telegram-connect"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("me/", ManageUserView.as_view(), name="profile"),
]

app_name = "user"
