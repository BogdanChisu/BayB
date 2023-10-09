from django.urls import path

from userextend import views

urlpatterns = [
    path('create_business_user/', views.BusinessUserCreateView.as_view(),
         name='create-business-user'),
]