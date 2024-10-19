from django.urls import path
from . import views


urlpatterns = [
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<int:user_id>/', views.profile_view, name='profile'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),

    path('follow_user/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('profile/<int:user_id>/followers/', views.followers_list, name='followers_list'),
    path('profile/<int:user_id>/following/', views.following_list, name='following_list'),

    path('signup/', views.signup, name='signup'),
    path('login/', views.CustomLoginView.as_view(redirect_authenticated_user=True, template_name='users/login.html'), name='login'),
    path('logout/', views.logout_confirm, name='logout'),
]