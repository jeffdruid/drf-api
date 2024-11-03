from django.db import models

class FlaggedContent(models.Model):
    post_id = models.CharField(max_length=100)  # Firebase post ID
    content = models.TextField()
    reason = models.CharField(max_length=255)
    user = models.CharField(max_length=255)  # Firebase user UID
    flagged_at = models.DateTimeField(auto_now_add=True)
    reviewed = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=False)  # New field to control post visibility

    def __str__(self):
        return f"Flagged by {self.user} for {self.reason}"

# TriggerWord model
class TriggerWord(models.Model):
    word = models.CharField(max_length=100, unique=True)  # Trigger word
    category = models.CharField(max_length=100)  # Category (e.g., "self-harm", "suicide-related")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.word} ({self.category})"
