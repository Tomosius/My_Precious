from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('create/', views.create_post, name='create_post'),
    path('lost/<slug:slug>/', views.post_detail_view, {'post_type': 'lost'},
         name='lost_post_details'),
    path('found/<slug:slug>/', views.post_detail_view, {'post_type': 'found'},
         name='found_post_details'),
    path('', views.view_all_posts, name='view_all_posts'),
    path('lost/', views.view_lost_posts, name='view_lost_posts'),
    path('found/', views.view_found_posts, name='view_found_posts'),
    path('posts/update/<post_type>/<slug>/', views.update_post,
         name='update_post'),
    path('delete_photo/<int:photo_id>/<str:post_type>/', views.delete_photo,
         name='delete_photo'),
    path('map/', views.map_all_posts, name='map_all_posts_view'),

]
