from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db import transaction
from .send_mail import send_confirmation_email
from .send_sms import sending_sms
from .serializers import UserSerializer, RegisterSerializer

User = get_user_model()


class RegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Используем транзакцию для обработки возможных ошибок
        with transaction.atomic():
            try:
                user = serializer.save()
                send_confirmation_email(user.email, user.activation_code)
            except Exception as e:
                # Если произошла ошибка при сохранении или отправке email, откатываем транзакцию
                transaction.set_rollback(True)
                return Response({"message": f"Error occurred: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserListView(ListAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        return UserSerializer


class ActivationView(APIView):
    def get(self, request):
        code = request.GET.get('u')
        user = get_object_or_404(User, activation_code=code)
        if not user.is_active:
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response('Регистрация прошла успешно!!!', status=200)
        else:
            return Response('User is already activated.', status=400)


class ActivationFromNumberView(APIView):
    def get(self, request):
        phone_number = request.GET.get('phone_number')
        user = get_object_or_404(User, phone_number=phone_number)
        user.is_active = True
        user.save()
        # Отправить SMS с уведомлением о успешной активации по номеру телефона
        sms_text = "Ваш аккаунт успешно активирован. Добро пожаловать!"
        sending_sms(text=sms_text, receiver=phone_number)

        return Response('Регистрация по номеру телефона прошла успешно!!!', status=200)


class LoginView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)


class RegistrationPhoneView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            try:
                user = serializer.save()
                sending_sms(user.phone_number, user.activation_code)
            except Exception as e:
                transaction.set_rollback(True)
                return Response({"message": f"Error occurred: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        return Response('Successfully registered', status=status.HTTP_201_CREATED)


class ActivationPhoneView(APIView):
    def post(self, request):
        phone = request.data.get('phone_number')
        code = request.data.get('activation_code')
        user = User.objects.filter(phone_number=phone, activation_code=code).first()
        if not user:
            return Response('No such user', status=400)
        user.activation_code = ''
        user.is_active = True
        user.save()
        return Response('Succesfuly activated', status=200)
