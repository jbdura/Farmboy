# comments/admin.py

from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'content', 'created_at', 'updated_at', 'total_likes')
    search_fields = ('user__username', 'post__title', 'content')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

    def total_likes(self, obj):
        return obj.total_likes
    total_likes.short_description = 'Total Likes'
