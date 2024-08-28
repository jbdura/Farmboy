from django.contrib import admin
from .models import Community, CommunityAdmin, CommunityMember


class CommunityAdminInline(admin.TabularInline):
    model = CommunityAdmin
    extra = 1


class CommunityMemberInline(admin.TabularInline):
    model = CommunityMember
    extra = 1


class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_public', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    list_filter = ('is_public', 'created_at', 'updated_at')
    inlines = [CommunityAdminInline, CommunityMemberInline]

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'is_public')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


admin.site.register(Community, CommunityAdmin)
