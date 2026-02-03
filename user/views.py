from string import ascii_letters
from random import choices

from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from user.serializers import UserSerializer, LogoutSerializer, TelegramConnectSerializer


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data["refresh_token"]

        try:
            token = RefreshToken(refresh_token)
            if token["user_id"] == str(request.user.id):
                token.blacklist()
            else:
                return Response(
                    {"error": "Not your token"}, status=status.HTTP_403_FORBIDDEN
                )
        except TokenError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_200_OK)


class CreateUserView(generics.GenericAPIView):
    permission_classes = ()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "user": serializer.data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class RegisterTelegramView(generics.GenericAPIView):
    serializer_class = TelegramConnectSerializer

    def get_object(self):
        return "".join(choices(ascii_letters, k=10))

    def get(self, request, *args, **kwargs):
        _id = self.request.user.telegram_id
        return Response({"telegram_id": _id if _id and _id.isdigit() else None}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        key = self.get_object()
        user_key = request.user.telegram_id
        serializer = self.get_serializer(data={"key": key})
        if serializer.is_valid() and not (user_key and user_key.isdigit()):
            serializer.save(user=request.user)
            return Response({"telegram_key": key}, status=status.HTTP_200_OK)
        return Response({"detail": "You are already registered"}, status=status.HTTP_403_FORBIDDEN)
