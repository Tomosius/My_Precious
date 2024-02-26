# posts/admin.py

from django.contrib import admin
from .models import Post, LostPost, FoundPost, LostPhoto, FoundPhoto
from polymorphic.admin import PolymorphicParentModelAdmin, \
    PolymorphicChildModelAdmin, PolymorphicChildModelFilter


# README: This module configures the Django admin interface for managing
# posts and photos in the 'posts' app. It includes custom admin classes to
# handle polymorphic models and integrate with Cloudinary for image management.

# Custom Admin Classes for Polymorphic Models

class PostAdmin(PolymorphicParentModelAdmin):
    """Admin interface for the Post model and its subclasses.

    Utilizes Django Polymorphic to seamlessly integrate child models.
    """
    base_model = Post
    child_models = (LostPost, FoundPost)
    list_filter = (
        PolymorphicChildModelFilter,)  # Enables filtering by child model type.
    list_display = ('title', 'user', 'event_date', 'post_type_display')

    def post_type_display(self, obj):
        """Displays the type of post in the admin list view."""
        return obj.post_type()

    post_type_display.short_description = 'Post Type'


class LostPostAdmin(PolymorphicChildModelAdmin):
    """Admin interface specifically for LostPost model."""
    base_model = LostPost
    show_in_index = True  # Display in the parent model's admin.
    list_display = ['title', 'user', 'event_date']


class FoundPostAdmin(PolymorphicChildModelAdmin):
    """Admin interface specifically for FoundPost model."""
    base_model = FoundPost
    show_in_index = True
    list_display = ['title', 'user', 'event_date']


# Admin classes for Photo models

class PhotoInline(admin.TabularInline):
    """Generic inline class for displaying photo instances related to a post."""
    extra = 1  # Controls the number of extra forms displayed.


class LostPhotoInline(PhotoInline):
    """Specific inline for LostPhoto instances."""
    model = LostPhoto


class FoundPhotoInline(PhotoInline):
    """Specific inline for FoundPhoto instances."""
    model = FoundPhoto


# Enhancing the LostPost and FoundPost admin with inlines for photos
class EnhancedLostPostAdmin(LostPostAdmin):
    inlines = [LostPhotoInline]


class EnhancedFoundPostAdmin(FoundPostAdmin):
    inlines = [FoundPhotoInline]


# Register models with the admin site
admin.site.register(Post, PostAdmin)
admin.site.register(LostPost, EnhancedLostPostAdmin)
admin.site.register(FoundPost, EnhancedFoundPostAdmin)
admin.site.register(
    LostPhoto)  # Assuming basic admin registration is sufficient
admin.site.register(
    FoundPhoto)  # Assuming basic admin registration is sufficient
