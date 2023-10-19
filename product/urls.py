from django.urls import path

from product import views

urlpatterns = [
    path('product_add', views.ProductCreateView.as_view(), name='product-add'),
]