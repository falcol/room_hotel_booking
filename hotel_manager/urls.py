from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('hotel/create/', views.create_hotel, name='hotel_create'),
]
