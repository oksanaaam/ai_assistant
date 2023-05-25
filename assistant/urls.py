from django.urls import path

from assistant.views import gpt_conversation

urlpatterns = [
    path("", gpt_conversation, name="chat"),
]

app_name = "assistant"
