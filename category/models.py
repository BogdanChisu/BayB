from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db import models

from userextend.models import CustomUser

class Category(models.Model):
    name = models.CharField(max_length=50)
    special_character = models.CharField(max_length=20, default='restart_alt')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name[:-1]


class HistoryCategory(models.Model):
    message = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.message