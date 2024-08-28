# userprofiles/admin.py
from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'location', 'created_at', 'updated_at')
    search_fields = ('user__username', 'name', 'location')
    readonly_fields = ('created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('user', 'name', 'bio', 'profile_image', 'location')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('user',)
        return self.readonly_fields


admin.site.register(UserProfile, UserProfileAdmin)
