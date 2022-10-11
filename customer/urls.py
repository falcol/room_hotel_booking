from django.urls import path
from . import views

urlpatterns = [
    path('my-book', views.my_book, name='my_book'),
    path('update-booking/<int:pk>', views.update_booking, name='update_booking'),
]
