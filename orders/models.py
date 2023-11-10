from django.contrib.auth.models import User
from django.db import models

from product.models import Product


class OrderCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart_item = models.BooleanField(default=False)
    wishlist_item = models.BooleanField(default=False)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def amount(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product


class PlaceOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product_list = models.JSONField(null=True)
    order_number = models.CharField(max_length=50)
    delivery_address = models.TextField(max_length=100)
    invoice_address = models.TextField(max_length=100)
    price = models.CharField(max_length=100)
    pdf_file = models.FileField(upload_to='order_pdf', null=True, blank=True)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.product_list

