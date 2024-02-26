from django.contrib import admin
from .models import UserProfile, SocialMediaLink, Language


# Define admin model for UserProfile with detailed configuration
class UserProfileAdmin(admin.ModelAdmin):
    """Admin view for UserProfile."""
    list_display = (
        'user', 'first_name', 'last_name', 'address', 'mobile_number',
        'website',
        'date_of_birth')
    search_fields = (
        'user__username', 'first_name', 'last_name', 'mobile_number')
    list_filter = ('date_of_birth',)
    ordering = ('user',)
    fieldsets = (
        (None, {'fields': ('user', 'user_photo')}),
        ('Personal Information',
         {'fields': ('first_name', 'last_name', 'date_of_birth')}),
        ('Contact Information',
         {'fields': ('address', 'mobile_number', 'website')}),
        ('Additional', {'fields': ('biography',)}),
    )


# Define admin model for SocialMediaLink
class SocialMediaLinkAdmin(admin.ModelAdmin):
    """Admin view for SocialMediaLink."""
    list_display = ('user_profile', 'name', 'url')
    search_fields = ('user_profile__user__username', 'name')
    list_filter = ('name',)


# Define admin model for Language
class LanguageAdmin(admin.ModelAdmin):
    """Admin view for Language."""
    list_display = ('user_profile', 'language')
    search_fields = ('user_profile__user__username', 'language')
    list_filter = ('language',)


# Register your models here with the custom admin models
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(SocialMediaLink, SocialMediaLinkAdmin)
admin.site.register(Language, LanguageAdmin)
