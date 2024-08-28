# forums/urls.py

from django.urls import path
from .views import ForumListCreateView, ForumDetailView

urlpatterns = [
    path('forums/', ForumListCreateView.as_view(), name='forum-list-create'),
    path('forums/<int:pk>/', ForumDetailView.as_view(), name='forum-detail'),
]
