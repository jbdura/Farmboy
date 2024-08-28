# likes/admin.py

from django.contrib import admin
from .models import Like

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_type', 'object_id', 'created_at')
    search_fields = ('user__username', 'content_type__model')
    list_filter = ('content_type', 'created_at')
    readonly_fields = ('created_at',)

    def content_object(self, obj):
        return obj.content_object
