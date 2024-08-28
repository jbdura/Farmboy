from django.contrib import admin
from .models import Forum


class ForumAdmin(admin.ModelAdmin):
    list_display = ('title', 'community', 'created_at', 'updated_at')
    search_fields = ('title', 'community__name')
    readonly_fields = ('created_at', 'updated_at')
    list_filter = ('community', 'created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('community', 'title')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


admin.site.register(Forum, ForumAdmin)
