import random
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db.models import EmailField


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **kwargs):
        phone_number = kwargs.get('phone_number', None)  # Извлечь phone_number из kwargs
        if not email:
            return ValueError('Email is required!!')
        email = self.normalize_email(email=email)
        user = self.model(email=email, **kwargs)
        user.create_activation_code()  # Создаем активационный код для email
        user.set_password(password)
        user.save()
        # if phone_number:
        #     # Если указан номер телефона, отправляем SMS
        #     sms_text = f'Чтобы зарегистрироваться введите сообщение код из сообщения\n{generate_sms_code()}'
        #     sending_sms(text=sms_text, receiver=phone_number)
        return user

    def create_user(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)
        return self._create_user(email, password, **kwargs)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    activation_code = models.CharField(max_length=255, blank=True)
    username = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    is_active = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=25, unique=True, blank=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self) -> EmailField:
        return self.email

    def create_activation_code(self):
        code = ''.join(str(random.randint(0, 9)) for _ in range(4))
        self.activation_code = code

