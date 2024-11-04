from django.db import models


class FlaggedContent(models.Model):
    # Model to store flagged content, with fields for post, 
    # comment, and reply IDs.
    post_id = models.CharField(max_length=100)  # Firebase post ID
    content = models.TextField()
    reason = models.CharField(max_length=255)
    user = models.CharField(max_length=255)  # Firebase user UID
    flagged_at = models.DateTimeField(auto_now_add=True)
    reviewed = models.BooleanField(default=False)
    is_visible = models.BooleanField(
        default=False
    )  # Control content visibility
    comment_id = models.CharField(
        max_length=100, null=True, blank=True
    )  # Optional comment ID
    reply_id = models.CharField(
        max_length=100, null=True, blank=True
    )  # Optional reply ID

    def __str__(self):
        return f"Flagged by {self.user} for {self.reason}"


# TriggerWord model
class TriggerWord(models.Model):
    # Model to store trigger words that will be flagged in content.
    word = models.CharField(max_length=100, unique=True)  # Trigger word
    category = models.CharField(max_length=100)  # Category (e.g., "self-harm")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.word} ({self.category})"
