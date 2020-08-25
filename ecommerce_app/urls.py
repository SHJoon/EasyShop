from django.urls import path
from . import views

urlpatterns = [
    path('login_index', views.login_index),
    path('register', views.register_user),
    path('login', views.login_user),
    path('logout', views.logout),
    path('', views.index),
]