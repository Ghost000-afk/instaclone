from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification


@login_required
def notifications_list(request):
    """
    Отображает список уведомлений для текущего пользователя.

    Args:
        request: HTTP-запрос для получения списка уведомлений.

    Returns:
        HttpResponse: HTML-страница со списком уведомлений, отсортированных по дате создания.
    """
    user_profile = request.user.userprofile
    notifications = Notification.objects.filter(recipient=user_profile).order_by('-timestamp')
    
    return render(request, 'notifications/notifications.html', {
        'notifications': notifications
    })





