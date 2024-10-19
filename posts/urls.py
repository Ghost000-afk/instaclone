from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('create_post/', views.create_post, name='create_post'),
    path('post_detail/<int:post_id>/', views.post_detail, name='post_detail'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),

    path('posts/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),
    path('posts/<int:post_id>/add_comment/<int:parent_id>/', views.add_comment, name='add_comment_reply'),

    path('search/', views.search_users, name='search_users'),
]

