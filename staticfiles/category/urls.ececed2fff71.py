from django.urls import path

from category import views

urlpatterns = [
    path("category_create/", views.CategoryCreateView.as_view(),
         name="category-create"),
    path("list_of_categories/", views.CategoryListView.as_view(),
         name="list-of-categories"),
    path("update_category/<int:pk>", views.CategoryUpdateView.as_view(),
         name="update-category"),
    path("delete_view.html/<int:pk>", views.CategoryDeleteView.as_view(),
         name="delete-view"),
    path("category_detail_view/<int:pk>", views.CategoryDetailView.as_view(),
         name="category-detail-view"),
]
