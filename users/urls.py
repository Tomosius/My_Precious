# users/urls.py

from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('user_login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('user_register/', views.user_register, name='user_register'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('edit_profile/', views.combined_update_user_profile, name='edit_profile'),
    path('delete_language/<int:language_id>/', views.delete_language, name='delete_language'),
    path('delete_social_media_link/<int:link_id>/', views.delete_social_media_link, name='delete_social_media_link'),
    path('add_language/', views.add_language, name='add_language'),
    path('add_social_media_link/', views.add_social_media_link, name='add_social_media_link'),


]
