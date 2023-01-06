"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path(r'^index$', views.index, name='index'),
    path('payment/<int:book_pk>', views.payment, name='payment'),
    re_path(r'^payment_ipn$', views.payment_ipn, name='payment_ipn'),
    re_path(r'^payment_return$', views.payment_return, name='payment_return'),
    re_path(r'^query$', views.query, name='query'),
    path('refund/<int:book_pk>', views.refund, name='payment_refund'),
]
