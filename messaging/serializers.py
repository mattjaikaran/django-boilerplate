from rest_framework import serializers
from core.emails import send_conversation_create_email
from core.models import CustomUser

from core.serializers import UserSerializer
from notifications.models import Notification
from .models import Conversation, Message
from notifications.constants import NEW_MESSAGE


class MessageSerializer(serializers.ModelSerializer):
    conversation = serializers.PrimaryKeyRelatedField(
        queryset=Conversation.objects.all(), required=False
    )
    sender = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), required=False
    )

    class Meta:
        model = Message
        fields = (
            "id",
            "sender",
            "recipient",
            "content",
            "conversation",
            "read",
            "datetime_created",
        )

    def create(self, validated_data):
        print(f"validated_data => {validated_data}")
        if validated_data["conversation"] is None:
            raise serializers.ValidationError("Conversation not found")
        else:
            conversation_data = validated_data.pop("conversation")
            try:
                message = Message.objects.create(**validated_data)
                conversation = Conversation.objects.get(id=conversation_data.id)
                conversation.messages.add(message)
                conversation.save()

                notification = Notification.objects.create(
                    recipient=message.recipient,
                    type=NEW_MESSAGE,
                )
                print(f"notification => {notification}")
                notification.save()

                return message
            except Conversation.DoesNotExist:
                raise serializers.ValidationError("Conversation not found")
            except Exception as e:
                print(f"Error creating conversation => {str(e)}")
                raise serializers.ValidationError(
                    f"Error creating conversation: {str(e)}"
                )


class ConversationSerializer(serializers.ModelSerializer):
    participants_ref = UserSerializer(source="participants", many=True, required=False)
    messages_ref = MessageSerializer(source="messages", many=True, required=False)

    class Meta:
        model = Conversation
        fields = (
            "id",
            "participants",
            "participants_ref",
            "messages",
            "messages_ref",
            "datetime_created",
        )

    def create(self, validated_data):
        try:
            conversation = Conversation.objects.create()
            for participant in validated_data["participants"]:
                conversation.participants.add(participant)
            conversation.save()

            # send email to support team
            context = {
                "recipient": validated_data["participants"][0].email,
                "sender": validated_data["participants"][1].email,
            }
            send_conversation_create_email(context)

            return conversation
        except Exception as e:
            print(f"Error creating conversation => {str(e)}")
            raise serializers.ValidationError(f"Error creating conversation: {str(e)}")

    def update(self, instance, validated_data):
        try:
            # add messages to conversation
            for message in validated_data.get("messages", []):
                instance.messages.add(message)
            instance.save()
            return instance
        except Exception as e:
            print(f"Error updating conversation => {str(e)}")
            raise serializers.ValidationError(f"Error updating conversation: {str(e)}")


class MessageFetchSerializer(serializers.ModelSerializer):
    last_message = serializers.IntegerField(required=False)

    class Meta:
        model = Message
        fields = "__all__"
