from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('dash', views.dash),
    path('logout', views.logout),
    path('new_rec', views.new_rec),
]