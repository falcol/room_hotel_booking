from django.urls import path

from . import views

urlpatterns = [
    path('my-book', views.my_book, name='my_book'),
    path('update-booking/<int:pk>', views.update_booking, name='update_booking'),
    path('booking/<int:book_pk>/guest-cancel', views.guest_cancel, name='guest_cancel'),
    path('customer/update', views.my_profile, name='update_profile'),
    path('customer/create_comment', views.create_comment, name='create_comment'),
    path('customer/create_rating', views.create_rating, name='create_rating'),
    path('customer/load_comments', views.load_comments, name='load_comments'),
]
