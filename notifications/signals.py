from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from posts.models import Post, Like, Comment
from users.models import UserProfile
from direct_messages.models import Message
from .models import Notification


@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    """
    Создает уведомление о лайке после сохранения объекта Like.

    Args:
        sender: Модель, которая инициировала сигнал (Like).
        instance: Экземпляр модели Like.
        created: Логическое значение, указывающее, был ли объект создан.
        **kwargs: Дополнительные аргументы.

    Returns:
        None: Создает объект уведомления для пользователя, получившего лайк.
    """
    if created:
        Notification.objects.create(
            sender=instance.user,  
            recipient=instance.post.user,  
            notification_type='like',
            post=instance.post
        )


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    """
    Создает уведомление о комментарии после сохранения объекта Comment.

    Args:
        sender: Модель, которая инициировала сигнал (Comment).
        instance: Экземпляр модели Comment.
        created: Логическое значение, указывающее, был ли объект создан.
        **kwargs: Дополнительные аргументы.

    Returns:
        None: Создает объект уведомления для пользователя, получившего комментарий.
    """
    if created:
        sender_profile = instance.user
        recipient_profile = instance.post.user

        Notification.objects.create(
            sender=sender_profile,
            recipient=recipient_profile,
            notification_type='comment',
            post=instance.post
        )


@receiver(m2m_changed, sender=UserProfile.followers.through)
def create_follow_unfollow_notification(sender, instance, action, reverse, pk_set, **kwargs):
    """
    Создает уведомление при подписке или отписке пользователя.

    Args:
        sender: Модель, которая инициировала сигнал (UserProfile.followers.through).
        instance: Экземпляр модели UserProfile, за которым следят или отписываются.
        action: Действие ('post_add' для подписки).
        reverse: Флаг обратного направления действия.
        pk_set: Набор первичных ключей объектов, участвующих в изменении связи.
        **kwargs: Дополнительные аргументы.

    Returns:
        None: Создает уведомление о подписке.
    """
    for pk in pk_set:
        follower = UserProfile.objects.get(pk=pk)
        if action == 'post_add':
            Notification.objects.create(
                sender=instance,   
                recipient=follower,  
                notification_type='follow'
            )


@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    """
    Создает уведомление о новом сообщении после сохранения объекта Message.

    Args:
        sender: Модель, которая инициировала сигнал (Message).
        instance: Экземпляр модели Message.
        created: Логическое значение, указывающее, было ли сообщение создано.
        **kwargs: Дополнительные аргументы.

    Returns:
        None: Создает уведомление для получателя сообщения.
    """
    if created:
        Notification.objects.create(
            sender=instance.sender,
            recipient=instance.conversation.participants.exclude(id=instance.sender.id).first(),
            notification_type='message',
            message=instance
        )
