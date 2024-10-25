from django.contrib import admin
from .models import FlaggedContent

@admin.register(FlaggedContent)
class FlaggedContentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post_id', 'reason', 'flagged_at', 'reviewed')  # Referencing the model fields
    search_fields = ('user__username', 'post_id', 'reason')
    list_filter = ('reviewed', 'flagged_at')  # These fields must exist in the model
