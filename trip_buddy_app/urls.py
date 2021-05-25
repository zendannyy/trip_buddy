from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('register', views.register),
    path('travels', views.travels),
    path('jointrip/<int:tripid>', views.jointrip),
    path('unjointrip/<int:tripid>', views.unjointrip),
    path('travels/add', views.addtravel),
    path('travels/save', views.recordtravel),
    path('destination/<int:tripid>', views.destination),
    path('delete/<int:tripid>', views.delete),
    path('logout', views.logout)
]