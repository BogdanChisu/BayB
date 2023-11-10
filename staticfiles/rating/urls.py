from django.urls import path

from rating import views

urlpatterns=[
    path('create_rating/', views.RatingCreateView.as_view(),
         name='create-rating')
]