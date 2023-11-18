from django.contrib.auth.models import User, AbstractUser
from django.db import models

from django.contrib.auth.models import BaseUserManager

from userextend.managers import CustomUserManager


class CustomUser(AbstractUser):
    company_name = models.CharField(max_length=50, blank=True, null=True)

    objects = CustomUserManager()

class History(models.Model):
    text = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
