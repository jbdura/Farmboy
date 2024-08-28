# posts/urls.py

from django.urls import path
from .views import PostListCreateView, PostDetailView, TagListCreateView

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<str:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('tags/', TagListCreateView.as_view(), name='tag-list-create'),
]
