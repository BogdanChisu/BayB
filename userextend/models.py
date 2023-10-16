from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class History(models.Model):
    text = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
