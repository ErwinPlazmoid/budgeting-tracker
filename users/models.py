from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    preferred_currency = models.CharField(max_length=3, default="USD")
