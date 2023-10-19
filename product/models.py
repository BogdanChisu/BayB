from django.db import models

from category.models import Category


# Create your models here.


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=20, default="n.a.")
    model_name = models.CharField(max_length=20, default="n.a.")
    description = models.TextField(max_length=400)
    image = models.ImageField(upload_to='product_pics')
    price = models.DecimalField(max_digits=4, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class HistoryProduct(models.Model):
    message = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.message