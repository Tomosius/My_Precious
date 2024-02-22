from django.urls import path
from . import views

app_name = 'conversations'

urlpatterns = [
    path('send_message/<str:recipient_username>/', views.send_message, name='send_message'),
    path('conversation_detail/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('conversations_list/', views.conversation_list, name='conversation_list'),
]

