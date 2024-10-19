from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from users.models import UserProfile
from .forms import PostForm, CommentForm
from .models import Post, Comment


@login_required
def create_post(request):
    """
    Создает новый пост пользователя.

    Args:
        request: HTTP-запрос с данными формы для создания поста.

    Returns:
        HttpResponse: HTML-страница с формой создания поста или перенаправление на главную страницу.
    """
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user.userprofile
            post.save()
            return redirect('index', user_id=request.user.userprofile.id)
    else:
        form = PostForm()

    return render(request, 'posts/create_post.html', {
        'form': form
    })


def index(request):
    """
    Отображает главную страницу с постами. Возможен поиск по заголовкам постов.

    Args:
        request: HTTP-запрос для отображения постов.
    
    Returns:
        HttpResponse: HTML-страница со списком постов.
    """
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(caption__icontains=query).order_by('-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')

    user_profile = None
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)

    return render(request, 'posts/index.html', {
        'posts': posts,
        'user_profile': user_profile
    })


@login_required
def post_detail(request, post_id):
    """
    Отображает подробную информацию о посте, включая комментарии. Обрабатывает добавление комментариев.

    Args:
        request: HTTP-запрос для отображения деталей поста.
        post_id (int): Идентификатор поста.

    Returns:
        HttpResponse: HTML-страница с детальной информацией о посте и формой комментария.
    """
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user.userprofile
            comment.save()
            return redirect('post_detail', post_id=post_id)
    else:
        form = CommentForm()

    return render(request, 'posts/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })


@login_required
def like_post(request, post_id):
    """
    Позволяет пользователю поставить или убрать лайк у поста.

    Args:
        request: HTTP-запрос для обработки лайков.
        post_id (int): Идентификатор поста.

    Returns:
        HttpResponse: Перенаправление на предыдущую страницу (или на главную, если реферер отсутствует).
    """
    post = get_object_or_404(Post, id=post_id)
    user_profile = request.user.userprofile
    like, created = post.likes.get_or_create(user=user_profile)
    if not created:
        like.delete()

    return redirect(request.META.get('HTTP_REFERER', 'index'))


@login_required
def add_comment(request, post_id, parent_id=None):
    """
    Добавляет комментарий или ответ на существующий комментарий к посту.

    Args:
        request: HTTP-запрос для добавления комментария.
        post_id (int): Идентификатор поста.
        parent_id (int, optional): Идентификатор родительского комментария, если это ответ.

    Returns:
        HttpResponse: HTML-страница с формой для добавления комментария или перенаправление на страницу поста.
    """
    post = get_object_or_404(Post, id=post_id)
    parent_comment = None

    if parent_id:
        parent_comment = get_object_or_404(Comment, id=parent_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user.userprofile
            comment.parent = parent_comment
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()

    return render(request, 'posts/post_detail.html', {
        'post': post,
        'form': form,
        'comments': post.comments.all()
    })


def search_users(request):
    """
    Ищет пользователей по имени пользователя (username).

    Args:
        request: HTTP-запрос для поиска пользователей.

    Returns:
        HttpResponse: HTML-страница с результатами поиска пользователей.
    """
    query = request.GET.get('q')

    if query:
        users = User.objects.filter(username__icontains=query)
    else:
        users = User.objects.none()

    return render(request, 'posts/search_results.html', {
        'users': users,
        'query': query
    })



