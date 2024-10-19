from django.db import models
from users.models import UserProfile  # Импортируем модель UserProfile


class Conversation(models.Model):
    participants = models.ManyToManyField(UserProfile)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        participants = ", ".join([user.user.username for user in self.participants.all()])
        # Ограничиваем вывод участников, если их слишком много
        return f'Conversation between {participants[:50]}...' if len(participants) > 50 else f'Conversation between {participants}'


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.user.username} on {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

    class Meta:
        ordering = ['created_at']  # Сообщения будут отображаться в порядке их создания
