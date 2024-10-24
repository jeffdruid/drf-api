from django.contrib import admin
from .models import FlaggedContent

class FlaggedContentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post_id', 'reason', 'flagged_at', 'reviewed')
    list_filter = ('reviewed', 'flagged_at')
    search_fields = ('user__username', 'post_id', 'reason')

    # Add actions to mark content as reviewed
    actions = ['mark_as_reviewed']

    def mark_as_reviewed(self, request, queryset):
        queryset.update(reviewed=True)
        self.message_user(request, "Selected flagged content has been marked as reviewed.")
    mark_as_reviewed.short_description = "Mark selected content as reviewed"

admin.site.register(FlaggedContent, FlaggedContentAdmin)
