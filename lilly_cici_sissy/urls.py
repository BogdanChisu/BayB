from django.urls import path

from lilly_cici_sissy import views

urlpatterns = [
    path('lillycicisissy', views.PuppiesView.as_view(),
         name='lilly-cici-sissy'),
]