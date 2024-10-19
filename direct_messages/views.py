from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from users.models import UserProfile
from .models import Conversation, Message


@login_required
def inbox(request):
    """
    Отображает список всех диалогов пользователя.

    Args:
        request: HTTP-запрос.

    Returns:
        HttpResponse: HTML-страница со списком диалогов пользователя, возможен поиск по имени пользователя.
    """
    user_profile = request.user.userprofile
    conversations = Conversation.objects.filter(participants=user_profile)

    query = request.GET.get('q')
    if query:
        conversations = conversations.filter(participants__user__username__icontains=query)

    return render(request, 'direct_messages/inbox.html', {
        'conversations': conversations,
        'query': query,
    })


@login_required
def start_conversation(request, user_id):
    """
    Создает новый диалог с указанным пользователем или возвращает существующий.

    Args:
        request: HTTP-запрос.
        user_id: Идентификатор пользователя, с которым необходимо начать диалог.

    Returns:
        HttpResponse: Перенаправление на страницу с деталями диалога.
    """
    other_user_profile = get_object_or_404(UserProfile, id=user_id)
    user_profile = request.user.userprofile
    conversation = Conversation.objects.filter(participants=user_profile).filter(participants=other_user_profile).first()

    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.set([user_profile, other_user_profile])

    return redirect('conversation_detail', conversation_id=conversation.id)


@login_required
def conversation_detail(request, conversation_id):
    """
    Отображает детали выбранного диалога.

    Args:
        request: HTTP-запрос.
        conversation_id: Идентификатор диалога.

    Returns:
        HttpResponse: HTML-страница с сообщениями диалога.
    """
    conversation = get_object_or_404(Conversation, id=conversation_id)
    return render(request, 'direct_messages/conversation_detail.html', {
        'conversation': conversation
    })


@login_required
def send_message(request, conversation_id):
    """
    Отправляет новое сообщение в выбранный диалог.

    Args:
        request: HTTP-запрос.
        conversation_id: Идентификатор диалога.

    Returns:
        HttpResponse: Перенаправление на страницу диалога после отправки сообщения.
    """
    conversation = get_object_or_404(Conversation, id=conversation_id)
    user_profile = request.user.userprofile

    if request.method == 'POST':
        text = request.POST.get('message')
        if text:
            Message.objects.create(conversation=conversation, sender=user_profile, text=text)

    return redirect('conversation_detail', conversation_id=conversation.id)


@login_required
def delete_conversation(request, conservation_id):
    """
    Удаляет выбранный диалог.

    Args:
        request: HTTP-запрос.
        conservation_id: Идентификатор диалога, который необходимо удалить.

    Returns:
        HttpResponse: HTML-страница с подтверждением удаления или перенаправление на страницу со списком диалогов.
    """
    conservation = get_object_or_404(Conversation, id=conservation_id)
    if request.method == 'POST':
        conservation.delete()
        return redirect('inbox')

    return render(request, 'direct_messages/delete_conservation.html', {
        'conservation': conservation
    })

