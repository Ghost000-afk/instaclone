from django.db import models
from django.contrib.auth.models import User
from users.models import UserProfile
from posts.models import Post
from direct_messages.models import Message


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
        ('message', 'Message'),
    )

    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_notifications', null=True)
    recipient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_notifications', null=True)  
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES, default='like')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender} {self.notification_type} {self.recipient}'