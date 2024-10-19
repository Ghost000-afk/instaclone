from rest_framework import serializers
from posts.models import Post, Comment, Like
from direct_messages.models import Conversation
from users.models import UserProfile

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields =['id', 'user', 'image', 'caption', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'



class DmSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['participants', 'updated_at']