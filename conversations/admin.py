from django.contrib import admin

from .models import Conversation, Message


# README: This module configures the Django admin interface for the
# Conversation and Message models. It enables administrators to manage
# conversations and messages directly from the admin panel.

# Named Constants Define constants for display options, if any, to improve
# readability and maintainability.

# Custom Admin Classes
class ConversationAdmin(admin.ModelAdmin):
    """Admin interface definition for Conversation model.

    Attributes:
        list_display (tuple): Columns to display in the admin list view.
        search_fields (tuple): Fields to be searched in the admin search box.
        list_filter (tuple): Fields to filter the list view.
    """
    # Customize the list display to improve admin usability
    list_display = ('id', 'display_participants', 'created_at', 'updated_at')
    search_fields = ('participants__username',)
    list_filter = ('created_at', 'updated_at')

    def display_participants(self, obj):
        """Return a comma-separated list of participant usernames."""
        return ", ".join([user.username for user in obj.participants.all()])

    display_participants.short_description = 'Participants'


class MessageAdmin(admin.ModelAdmin):
    """Admin interface definition for Message model.

    Attributes:
        list_display (tuple): Columns to display in the admin list view.
        search_fields (tuple): Fields to be searched in the admin search box.
        list_filter (tuple): Fields to filter the list view.
        ordering (tuple): Default ordering of the list view.
    """
    list_display = ('id', 'conversation', 'sender', 'short_text', 'created_at')
    search_fields = ('text', 'sender__username', 'conversation__id')
    list_filter = ('created_at', 'sender')
    ordering = ('created_at',)

    def short_text(self, obj):
        """Return the first 50 characters of the message text."""
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text

    short_text.short_description = 'Text'


# Register models with their respective admin class
admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Message, MessageAdmin)
