from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet,CommentViewSet, LikeViewSet, UserViewSet, ConversationViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'users', UserViewSet)
router.register(r'conversations', ConversationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
