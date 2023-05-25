import openai
from django.shortcuts import render
from .models import Conversation


def generate_response(prompt):
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = completions.choices[0].text
    return message


def gpt_conversation(request):
    if request.method == "POST":
        user_input = request.POST.get("user_input")

        if not user_input.strip():
            return render(request, "assistant/chat.html", {"empty_input_error": True})

        previous_conversations = Conversation.objects.all().order_by("-created_at")[:5]
        context = "\n".join([conv.user_input for conv in previous_conversations])
        conversation = f"{context}\nUser: {user_input}"

        ai_response = generate_response(conversation)

        Conversation.objects.create(user_input=user_input, ai_response=ai_response)

        return render(
            request,
            "assistant/chat.html",
            {
                "user_input": user_input,
                "ai_response": ai_response,
                "previous_conversations": previous_conversations,
            },
        )

    return render(request, "assistant/chat.html")
