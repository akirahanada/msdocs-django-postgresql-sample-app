from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/', views.details, name='details'),
    path('create', views.create_restaurant, name='create_restaurant'),
    path('add', views.add_restaurant, name='add_restaurant'),
    path('review/<int:id>', views.add_review, name='add_review'),
    path('restaurant/<int:id>/delete/', views.delete_restaurant, name='delete_restaurant'),
    path('restaurant/<int:id>/update/', views.update_restaurant, name='update_restaurant'),
    path('review/<int:id>/delete/', views.delete_review, name='delete_review'),
    path('review/<int:id>/update/', views.update_review, name='update_review'),
]

