# users/urls.py

from django.urls import path
from . import views


app_name = 'users'

urlpatterns = [
    path('user_login/', views.UserLoginView.as_view(), name='user_login'),
    path('user_register/', views.UserRegisterView.as_view(),
         name='user_register'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('edit_profile/', views.UpdateProfileView.as_view(),
         name='edit_profile'),
    path('delete_language/<int:language_id>/', views.delete_language, name='delete_language'),
    path('delete_social_media_link/<int:link_id>/', views.delete_social_media_link, name='delete_social_media_link'),
    path('add_language/', views.add_language, name='add_language'),
    path('add_social_media_link/', views.add_social_media_link, name='add_social_media_link'),
    path('list_users/', views.list_users, name='list_users'),
    path('logout/', views.user_logout, name='user_logout')





]
