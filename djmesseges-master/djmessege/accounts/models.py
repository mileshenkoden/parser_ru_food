
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'username'  # Авторизація через username
    REQUIRED_FIELDS = ['email']  # Email вимагається для міграцій, але може бути не обов'язковим для реєстрації
