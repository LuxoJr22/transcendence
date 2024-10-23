from django.urls import path
from .views import MessageListView, ChatHistoryView

urlpatterns = [
	path('chat/messages/<int:user_id>/', MessageListView.as_view(), name='message_list'),
	path('chat/history/', ChatHistoryView.as_view(), name='chat_history'),
]
