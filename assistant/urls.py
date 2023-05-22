from django.urls import path

from assistant.views import chat_view

urlpatterns = [
    path("", chat_view, name="chat"),
]

app_name = "assistant"
