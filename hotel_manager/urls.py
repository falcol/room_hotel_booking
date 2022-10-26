from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('hotel/create/', views.create_hotel, name='hotel_create'),
    path('hotel/my', views.my_hotels, name='my_hotel'),
    path('hotel/<int:pk>/rooms/', views.hotel_rooms, name='hotel_rooms'),
    path('hotel/<int:pk>/my_rooms/', views.my_hotel_rooms, name='my_hotel_rooms'),
    path('hotel/<int:hotel_pk>/new-room/', views.create_room_hotel, name='hotel_new_room'),
    path('hotel/<int:hotel_pk>/room-price/', views.create_room_price, name='hotel_room_price'),
    path('hotel/<int:hotel_pk>/books/', views.my_hotel_book, name='my_hotel_book'),
    path('hotel/<int:hotel_pk>/update-hotel/', views.update_hotel_info, name='update_hotel_info'),
    path('hotel/<int:room_pk>/update-room/', views.update_room_hotel, name='update_room_hotel'),
    path('hotel/<int:room_pk>/empty-room/', views.set_room_empty, name='set_room_empty'),
    path('hotel/<int:hotel_pk>/dashboard/', views.dashboard, name='dashboard'),
]
