from django.urls import path
from . import views

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),

    path('start_conversation/<int:user_id>/', views.start_conversation, name='start_conversation'),
    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('delete_conservation/<int:conservation_id>/', views.delete_conversation, name='delete_conversation'),

    path('send_message/<int:conversation_id>/', views.send_message, name='send_message'),
]