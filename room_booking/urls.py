from django.urls import path

from . import views

urlpatterns = [
    path('hotel/room/<int:pk>', views.create_booking, name='create_booking'),
    path('hotel/room/<int:book_pk>/checkout', views.booking_checkout, name='booking_checkout'),
    path('book/notify', views.booking_notify, name='booking_notify'),
    path('book/<int:book_pk>/checkin', views.guest_check_in, name='guest_check_in'),
    path('book/<int:book_pk>/hotel-cancel', views.hotel_guest_cancel, name='hotel_guest_cancel'),
]
