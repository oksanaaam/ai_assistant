import openai
from .models import Conversation

from urllib.request import Request

from django.http import HttpResponse
from django.shortcuts import render


def chat_view(request: Request) -> HttpResponse:
    if request.method == "POST":
        user_input = request.POST.get("user_input")

        # Отримання попередніх розмов з пам'яті
        previous_conversations = Conversation.objects.all().order_by("-created_at")[:5]
        context = '\n'.join([f"User: {c.user_input}\nAI: {c.ai_response}" for c in previous_conversations])

        # ai_response = ai.predict(user_input, context=context)

        # Виклик GPT-3.5-turbo для отримання відповіді
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input},
                {"role": "assistant", "content": context}
            ],
            max_tokens=100
        )
        ai_response = completion.choices[0].message.content

        # Збереження поточної розмови
        conversation = Conversation(user_input=user_input, ai_response=ai_response)
        conversation.save()

        # Передача даних до шаблону для відображення
        context = {
            "user_input": user_input,
            "ai_response": ai_response,
            "previous_conversations": previous_conversations
        }
        return render(request, "assistant/chat.html", context)

    return render(request, "assistant/chat.html")
