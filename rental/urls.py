from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('cars/', views.car_list, name='car_list'),
    path('cars/<int:car_id>/', views.car_detail, name='car_detail'),
    path('cars/<int:car_id>/book/', views.book_car, name='book_car'),
    path('dashboard/', views.dashboard, name='dashboard'),
     path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

]