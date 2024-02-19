# users/urls.py

from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('user_login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('user_register/', views.user_register, name='user_register'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('profile_update/', views.update_profile,
         name='update_profile'),

]
