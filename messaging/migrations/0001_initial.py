# Generated by Django 4.2.3 on 2023-11-15 19:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("datetime_created", models.DateTimeField(auto_now_add=True)),
                ("last_edited", models.DateTimeField(auto_now=True)),
                ("is_removed", models.BooleanField(default=False)),
                ("content", models.TextField(max_length=512)),
                ("read", models.BooleanField(default=False)),
                (
                    "recipient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="messages_received",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="messages_sent",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Conversation",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("datetime_created", models.DateTimeField(auto_now_add=True)),
                ("last_edited", models.DateTimeField(auto_now=True)),
                ("is_removed", models.BooleanField(default=False)),
                (
                    "messages",
                    models.ManyToManyField(
                        blank=True,
                        related_name="conversation_messages",
                        to="messaging.message",
                    ),
                ),
                (
                    "participants",
                    models.ManyToManyField(
                        related_name="conversations", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
