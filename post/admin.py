# posts/admin.py
from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import Post, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'post_type', 'forum', 'created_at', 'updated_at', 'total_likes')
    list_filter = ('post_type', 'created_at', 'updated_at')
    search_fields = ('author__username', 'content')
    raw_id_fields = ('author', 'forum')
    filter_horizontal = ('tags',)
    readonly_fields = ('total_likes', 'created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        if obj.post_type == 'forum' and not obj.tags.exists():
            raise ValidationError("Forum posts must have at least one tag.")
        super().save_model(request, obj, form, change)

# from django.contrib import admin
# from .models import Post
# # Register your models here.
#
# admin.site.register(Post)
# # admin.site.register(Like)
# # admin.site.register(Comment)