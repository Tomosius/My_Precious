from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('create/', views.create_post, name='create_post'),
    path('lost/<slug:slug>/', views.post_detail_view, {'post_type': 'lost'}, name='lost_post_details'),
    path('found/<slug:slug>/', views.post_detail_view, {'post_type': 'found'}, name='found_post_details'),
    path('', views.view_all_posts, name='view_all_posts'),
    path('lost/', views.view_lost_posts, name='view_lost_posts'),
    path('found/', views.view_found_posts, name='view_found_posts'),
]
