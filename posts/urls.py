from django.urls import path
from .models import Posts

from .views import (
    post_list_api_view,
    post_detail_api_view,
    comment_list_api_view,
    comment_detail_api_view,
)

urlpatterns = [
    path('posts/', post_list_api_view, name='post-list'),
    path('posts/<int:post_id>/', post_detail_api_view, name='post-detail'),

    path('posts/<int:post_id>/comments/', comment_list_api_view, name='comment-list'),
    path('comments/<int:comment_id>/', comment_detail_api_view, name='comment-detail'),
]
