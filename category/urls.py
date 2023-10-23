from django.urls import path

from category import views

urlpatterns = [
    path("category_create/", views.CategoryCreateView.as_view(),
         name="category-create"),
    path("list_of_categories/", views.CategoryListView.as_view(),
         name="list-of-categories"),
]
