# urls.py is a file that contains URL patterns for the project.

from django.contrib import admin
from django.urls import path, include
from posts.views import view_all_posts

urlpatterns = [
    # Including conversations app URLS
    path('conversations/', include('conversations.urls')),

    # Including posts app URLS
    path('posts/', include('posts.urls')),

    # Including users app URLS
    path('users/', include('users.urls')),

    # Home page
    path('', view_all_posts, name='home'),

    # Admin URL
    path('admin/', admin.site.urls),
]
