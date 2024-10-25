import firebase_admin
from firebase_admin import firestore
from django.contrib import admin
from .models import FlaggedContent
from django.contrib import messages

# Initialize Firebase if it’s not already initialized
if not firebase_admin._apps:
    firebase_admin.initialize_app()

# Reference to Firestore
db = firestore.client()

@admin.action(description="Approve and make visible")
def approve_flagged_content(modeladmin, request, queryset):
    approved_posts = []
    for flagged_content in queryset:
        try:
            # Update Firestore document's `is_visible` field
            post_ref = db.collection("Posts").document(flagged_content.post_id)
            post_ref.update({"is_visible": True})

            # Update local Django database
            flagged_content.is_visible = True
            flagged_content.reviewed = True
            flagged_content.save()
            approved_posts.append(flagged_content.post_id)

        except Exception as e:
            messages.error(request, f"Failed to approve {flagged_content.post_id}: {e}")

    # Provide feedback to the admin
    if approved_posts:
        messages.success(request, f"{len(approved_posts)} post(s) approved and made visible.")

class FlaggedContentAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'reason', 'user', 'flagged_at', 'reviewed', 'is_visible')
    actions = [approve_flagged_content]
    readonly_fields = ['post_id', 'content', 'reason', 'user', 'flagged_at']

    def has_change_permission(self, request, obj=None):
        # Prevent editing of any fields other than the block/allow actions
        return False

admin.site.register(FlaggedContent, FlaggedContentAdmin)
