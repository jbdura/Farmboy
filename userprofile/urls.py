# userprofile/urls.py

from django.urls import path
from userprofile.views import UserProfileDetail

urlpatterns = [
    # Other paths
    path('api/profile/<int:pk>/', UserProfileDetail.as_view(), name='userprofile-detail'),
]
