from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('wall', views.wall),
    path('register', views.register),
    path('login', views.login),
    path('loginpage', views.loginpage),
    path('logout', views.logout),
    path('createpost', views.createpost),
    path('createcomment', views.createcomment),
]