from django.contrib.auth.models import User
from django.db import models

from product.models import Product
from userextend.models import CustomUser


# Create your models here.

class Rating(models.Model):
    rating_options = (
        ('1', 'Completely dissatisfied'),
        ('2', 'Dissatisfied'),
        ('3', 'Acceptable'),
        ('4', 'Satisfied'),
        ('5', 'Very satisfied'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating_val = models.CharField(choices=rating_options, max_length=1,
                                  default=5)
    description = models.TextField(max_length=300, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.rating_val} {self.user.first_name}'
