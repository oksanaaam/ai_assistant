from assistant.views import generate_response, gpt_conversation
from django.test import TestCase
from django.urls import reverse, resolve
from django.test import Client

from .models import Conversation


class GPTConversationTest(TestCase):
    def setUp(self):
        self.url = reverse("assistant:chat")

    def test_reverse_url(self):
        self.assertEqual(resolve(self.url).func, gpt_conversation)

    def test_gpt_conversation_view(self):
        client = Client()
        response = client.post(self.url, {"user_input": "Hi"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("user_input", response.context)
        self.assertIn("ai_response", response.context)

    def test_conversation_model(self):
        conversation = Conversation.objects.create(
            user_input="Hi", ai_response="Hello!"
        )
        self.assertEqual(conversation.user_input, "Hi")
        self.assertEqual(conversation.ai_response, "Hello!")
        self.assertIsNotNone(conversation.created_at)

    def test_create_conversation(self):
        client = Client()
        response = client.post(self.url, {"user_input": "Hi"}, follow=True)
        self.assertEqual(response.status_code, 200)

        conversations = Conversation.objects.all()
        self.assertEqual(len(conversations), 1)
        self.assertEqual(conversations[0].user_input, "Hi")

    def test_chat_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "assistant/chat.html")

    def test_chat_view_post_empty_input(self):
        response = self.client.post(self.url, {"user_input": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "assistant/chat.html")
        self.assertContains(response, "Please enter your question.")

    def test_chat_view_post_valid_input(self):
        response = self.client.post(self.url, {"user_input": "Hello"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "assistant/chat.html")
        self.assertContains(response, "User: Hello")
        self.assertIn("AI:", response.content.decode())
        self.assertEqual(Conversation.objects.count(), 1)

    def test_generate_response(self):
        prompt = "Привіт, як можу допомогти?"
        response = generate_response(prompt)
        self.assertIsInstance(response, str)
        self.assertNotEqual(response, "")


class ChatTemplateTest(TestCase):
    def setUp(self):
        self.url = reverse("assistant:chat")

    def test_user_input_and_ai_response_displayed(self):
        response = self.client.post(self.url, {"user_input": "Hello"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "User: Hello")
        self.assertIn("AI:", response.content.decode())

    def test_empty_input_error_displayed(self):
        response = self.client.post(self.url, {"user_input": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter your question.")

    def test_microphone_button_functionality(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="microphoneBtn" class="inactive"')
        self.assertContains(
            response, "navigator.mediaDevices.getUserMedia({ audio: true })"
        )

    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "assistant/chat.html")
