from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    # URL for creating a new post
    path('create/', views.create_post, name='create_post'),

    # Detail view URLs for lost and found posts, using slugs for identification
    path('lost/<slug:slug>/', views.post_detail_view, {'post_type': 'lost'},
         name='lost_post_details'),
    path('found/<slug:slug>/', views.post_detail_view, {'post_type': 'found'},
         name='found_post_details'),

    # URL for viewing all posts
    path('', views.view_all_posts_list, name='view_all_posts'),

    # URLs for viewing all lost or found posts
    path('lost/', views.view_lost_posts, name='view_lost_posts'),
    path('found/', views.view_found_posts, name='view_found_posts'),

    # URL for updating a post, supporting both lost and found types
    path('update/<post_type>/<slug>/', views.update_post, name='update_post'),

    # URL for deleting a photo from a post
    path('delete_photo/<int:photo_id>/<str:post_type>/', views.delete_photo,
         name='delete_photo'),

    # URL for viewing a map of all posts
    path('map/', views.map_all_posts, name='map_all_posts_view'),




]
