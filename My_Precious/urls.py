# urls.py is a file that contains URL patterns for the project.

from django.contrib import admin
from django.urls import path, include
from users.views import user_login

urlpatterns = [
    # Including users app URLS
    path('users/', include('users.urls')),

    # Home page
    path('', user_login, name='home'),
    # Admin URL
    path('admin/', admin.site.urls),
]
