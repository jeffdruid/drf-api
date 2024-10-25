from django.contrib import admin
from .models import FlaggedContent

@admin.action(description='Allow selected content (make visible)')
def allow_content(modeladmin, request, queryset):
    queryset.update(is_visible=True, reviewed=True)

@admin.action(description='Block selected content (keep hidden)')
def block_content(modeladmin, request, queryset):
    queryset.update(is_visible=False, reviewed=True)

class FlaggedContentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post_id', 'reason', 'flagged_at', 'reviewed', 'is_visible']
    list_filter = ['reviewed', 'flagged_at']
    readonly_fields = ['post_id', 'content', 'reason', 'user', 'flagged_at']  # Make fields non-editable
    actions = [allow_content, block_content]  # Add actions to allow/block content

    def has_change_permission(self, request, obj=None):
        # Prevent editing of any fields other than the block/allow actions
        return False

admin.site.register(FlaggedContent, FlaggedContentAdmin)
