from django.urls import path

from product import views

urlpatterns = [
    path('product_add', views.ProductCreateView.as_view(), name='product-add'),
    path('list_of_products', views.ProductListView.as_view(),
         name='list-of-products'),
    path('update_product/<int:pk>', views.ProductUpdateView.as_view(),
         name='update-product'),
    path('product_delete_modal/<int:pk>', views.delete_product_modal,
         name='product-delete-modal'),
    path('product_detail/<int:pk>', views.ProductDetailView.as_view(),
         name='product-details'),
    path('products_by_category/<int:pk>', views.products_by_category, name='products-by-category'),
]