from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Conversation

User = get_user_model()


class MessageModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email="user1@example.com",
            password="password1",
            first_name="User1",
            last_name="Last1",
        )
        self.user2 = User.objects.create_user(
            email="user2@example.com",
            password="password2",
            first_name="User2",
            last_name="Last2",
        )

    def test_message_creation(self):
        message = Message.objects.create(
            sender=self.user1,
            recipient=self.user2,
            content="Hello, how are you?",
        )
        self.assertEqual(
            str(message),
            f"Message: Hello, how are you? - From User1 Last1 to User2 Last2",
        )


class ConversationModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email="user1@example.com",
            password="password1",
            first_name="User1",
            last_name="Last1",
        )
        self.user2 = User.objects.create_user(
            email="user2@example.com",
            password="password2",
            first_name="User2",
            last_name="Last2",
        )

    def test_conversation_creation(self):
        conversation = Conversation.objects.create()
        conversation.participants.add(self.user1, self.user2)
        self.assertEqual(
            str(conversation),
            f"Conversation: Conversation between - User1 Last1, User2 Last2",
        )

    def test_conversation_participants_list(self):
        conversation = Conversation.objects.create()
        conversation.participants.add(self.user1, self.user2)
        self.assertEqual(
            conversation.participants_list(),
            "Conversation between - User1 Last1, User2 Last2",
        )
