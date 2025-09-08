# chat/urls.py
from django.urls import path
from .views import ChatPageView, ChatAPI

app_name = "chats"
urlpatterns = [
    path("", ChatPageView.as_view(), name="chat_page"),
    path("api/", ChatAPI.as_view(), name="chat_api"),
]
