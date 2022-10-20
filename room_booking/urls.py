from django.urls import path

from . import views

urlpatterns = [
    path('hotel/room/<int:pk>', views.create_booking, name='create_booking'),
    path('hotel/room/<int:book_pk>/checkout', views.booking_checkout, name='booking_checkout'),
]
