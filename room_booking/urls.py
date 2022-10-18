from django.urls import path

from . import views

urlpatterns = [
    path('hotel/room/<int:pk>', views.create_booking, name='create_booking'),
]
