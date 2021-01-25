from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create, name='create'),
    path('edit/<str:movie_id>/', views.update, name='update'),
    path('delete/<str:movie_id>/', views.delete, name='delete'),
]
