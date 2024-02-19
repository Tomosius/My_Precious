# users/urls.py

from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('user_login/', views.user_login, name='user_login'),
]