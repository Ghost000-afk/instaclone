from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy

from .forms import UserProfileForm, SignUpForm
from .models import UserProfile
from posts.models import Post


def signup(request):
    """
    Обрабатывает регистрацию нового пользователя.

    Args:
        request: HTTP-запрос с данными формы регистрации.

    Returns:
        HttpResponse: HTML-страница с формой регистрации или перенаправление на страницу профиля.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('profile', user_id=user.id)
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


class CustomLoginView(LoginView):
    """
    Обрабатывает вход пользователя.

    Args:
        request: HTTP-запрос на вход в систему.

    Returns:
        HttpResponse: HTML-страница с формой входа или перенаправление на главную страницу.
    """
    template_name = 'users/login.html'
    next_page = reverse_lazy('index')


def logout_confirm(request):
    """
    Подтверждение выхода пользователя из аккаунта.

    Args:
        request: HTTP-запрос на подтверждение выхода.

    Returns:
        HttpResponse: HTML-страница с подтверждением выхода или перенаправление на главную страницу.
    """
    if request.method == 'POST':
        logout(request)
        return redirect('index')
    return render(request, 'users/logout_confirm.html')


@login_required
def profile(request, user_id):
    """
    Отображает профиль пользователя и статус подписки на него.

    Args:
        request: HTTP-запрос для просмотра профиля.
        user_id (int): Идентификатор пользователя, чей профиль просматривается.

    Returns:
        HttpResponse: HTML-страница с профилем пользователя.
    """
    user_profile = get_object_or_404(UserProfile, id=user_id)
    current_user_profile = request.user.userprofile
    is_following = user_profile.followers.filter(id=current_user_profile.id).exists()

    return render(request, 'users/profile.html', {
        'user_profile': user_profile,
        'is_following': is_following
    })


@login_required
def edit_profile(request):
    """
    Обрабатывает редактирование профиля пользователя.

    Args:
        request: HTTP-запрос на редактирование профиля.

    Returns:
        HttpResponse: HTML-страница с формой редактирования профиля или перенаправление на страницу профиля.
    """
    user_profile = request.user.userprofile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile', user_id=user_profile.id)
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def delete_post(request, post_id):
    """
    Удаляет пост пользователя.

    Args:
        request: HTTP-запрос на удаление поста.
        post_id (int): Идентификатор поста, который нужно удалить.

    Returns:
        HttpResponse: HTML-страница с подтверждением удаления поста или перенаправление на страницу профиля.
    """
    post = get_object_or_404(Post, id=post_id)

    if post.user != request.user.userprofile:
        return redirect('profile', user_id=request.user.userprofile.id)

    if request.method == 'POST':
        post.delete()
        return redirect('profile', user_id=request.user.userprofile.id)

    return render(request, 'users/confirm_delete.html', {'post': post})


@login_required
def follow_user(request, user_id):
    """
    Подписка или отписка от пользователя.

    Args:
        request: HTTP-запрос на подписку/отписку.
        user_id (int): Идентификатор пользователя, на которого нужно подписаться/отписаться.

    Returns:
        HttpResponse: Перенаправление на страницу профиля пользователя.
    """
    user_to_follow = get_object_or_404(UserProfile, id=user_id)
    user_profile = request.user.userprofile

    if user_to_follow in user_profile.following.all():
        user_profile.following.remove(user_to_follow)
    else:
        user_profile.following.add(user_to_follow)

    return redirect('profile', user_id=user_id)


@login_required
def unfollow_user(request, user_id):
    """
    Отписка от пользователя.

    Args:
        request: HTTP-запрос на отписку.
        user_id (int): Идентификатор пользователя, от которого нужно отписаться.

    Returns:
        HttpResponse: Перенаправление на страницу профиля пользователя.
    """
    user_to_unfollow = get_object_or_404(UserProfile, id=user_id)
    user_to_unfollow.followers.remove(request.user.userprofile)
    request.user.userprofile.followers.remove(user_to_unfollow)
    return redirect('profile', user_id=user_id)


@login_required
def profile_view(request, user_id):
    """
    Отображает профиль пользователя и статус подписки.

    Args:
        request: HTTP-запрос для просмотра профиля.
        user_id (int): Идентификатор пользователя, чей профиль просматривается.

    Returns:
        HttpResponse: HTML-страница с профилем пользователя и статусом подписки.
    """
    user_profile = get_object_or_404(UserProfile, id=user_id)
    user = request.user.userprofile

    return render(request, 'users/profile.html', {
        'user_profile': user_profile,
        'is_following': user_profile in user.following.all()
    })


def followers_list(request, user_id):
    """
    Отображает список подписчиков пользователя.

    Args:
        request: HTTP-запрос на отображение списка подписчиков.
        user_id (int): Идентификатор пользователя, чьи подписчики отображаются.

    Returns:
        HttpResponse: HTML-страница со списком подписчиков.
    """
    user_profile = get_object_or_404(UserProfile, id=user_id)
    followers = user_profile.followers.all()

    query = request.GET.get('q')
    if query:
        followers = followers.filter(user__username__icontains=query)

    return render(request, 'users/followers_list.html', {
        'user_profile': user_profile,
        'followers': followers,
        'query': query,
    })


def following_list(request, user_id):
    """
    Отображает список пользователей, на которых подписан данный пользователь.

    Args:
        request: HTTP-запрос на отображение списка подписок.
        user_id (int): Идентификатор пользователя, чьи подписки отображаются.

    Returns:
        HttpResponse: HTML-страница со списком пользователей, на которых подписан пользователь.
    """
    user_profile = get_object_or_404(UserProfile, id=user_id)
    following = user_profile.following.all()

    query = request.GET.get('q')
    if query:
        following = following.filter(user__username__icontains=query)

    return render(request, 'users/following_list.html', {
        'user_profile': user_profile,
        'following': following,
        'query': query,
    })


