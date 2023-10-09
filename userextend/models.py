from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class BusinessUser(User):
    company = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.company}'
