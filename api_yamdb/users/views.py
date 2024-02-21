from rest_framework import views, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from users.serializers import (
    TokenSerializer,
    SignupSerializer
)
from users.models import User


class LoginAPIView(views.APIView):
    """Обрабатываем запросы к /auth/token."""
    permission_classes = (AllowAny,)
    serializer_class = TokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignupViewSet(views.APIView):
    """Обрабатываем запросы к /auth/signup."""
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        При получении запроса данные проверяются сериализатором.
        После пытаемся получить объект, если он не существует создаем его.
        Отправляем код и ответ.
        """
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            current_user = User.objects.get(**serializer.validated_data)
        except User.DoesNotExist:
            current_user = serializer.save()
        current_user.send_confirmation_code()
        return Response(serializer.data, status=status.HTTP_200_OK)
