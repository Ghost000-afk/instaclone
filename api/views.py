from rest_framework import viewsets
from users.models import UserProfile
from direct_messages.models import Conversation
from posts.models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, UserSerializer, DmSerializer
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination


class PostViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для просмотра и редактирования постов.

    URL: /api/posts/

    Методы:
        - GET: Получить список всех постов.
        - POST: Создать новый пост.

    Разрешения:
        - AllowAny: Доступен любому пользователю.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]


class CommentViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для просмотра и редактирования комментариев.

    URL: /api/comments/

    Методы:
        - GET: Получить список всех комментариев.
        - POST: Создать новый комментарий.

    Разрешения:
        - AllowAny: Доступен любому пользователю.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]


class LikeViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для просмотра и редактирования лайков.

    URL: /api/likes/

    Методы:
        - GET: Получить список всех лайков.
        - POST: Поставить лайк посту.

    Разрешения:
        - AllowAny: Доступен любому пользователю.
    """
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [AllowAny]


class UserViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для просмотра и редактирования пользователей.

    URL: /api/users/

    Методы:
        - GET: Получить список всех пользователей.
        - POST: Создать нового пользователя.

    Разрешения:
        - AllowAny: Доступен любому пользователю.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class PostPagination(PageNumberPagination):
    """
    Кастомная пагинация для постов.

    URL: /api/posts/?page=1&page_size=5

    Параметры:
        - page: Номер страницы для получения (по умолчанию 1).
        - page_size: Количество постов на странице (по умолчанию 5, максимум 10).
    """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10
    

class ConversationViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для просмотра и редактирования разговоров.

    URL: /api/conversations/

    Методы:
        - GET: Получить список всех разговоров.
        - POST: Начать новый разговор.

    Разрешения:
        - AllowAny: Доступен любому пользователю.
    """
    queryset = Conversation.objects.all()
    serializer_class = DmSerializer
    permission_classes = [AllowAny]