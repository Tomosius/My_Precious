# Description: This file contains the URL patterns for the messaging app.

from django.urls import path
from .views import (SendMessageView, ConversationDetailView,
                    ConversationListView)


app_name = 'conversations'

urlpatterns = [
    path('send_message/<str:recipient_username>/', SendMessageView.as_view(), name='send_message'),
    path('conversation/<int:pk>/', ConversationDetailView.as_view(), name='conversation_detail'),
    path('conversations/', ConversationListView.as_view(), name='conversations_list'),

]
