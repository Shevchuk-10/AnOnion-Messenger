from django.urls import path
from .views import MessageList, MessageDetail
from . import views


urlpatterns = [
    path('chat/', views.chat_view, name='chat'),
    path('messages/', MessageList.as_view(), name='api_message_list'),
    path('messages/<int:pk>/', MessageDetail.as_view(), name='message_detail'),
]


