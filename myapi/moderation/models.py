from django.db import models
from django.contrib.auth.models import User

class FlaggedContent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.CharField(max_length=100)  # Store Firestore post ID
    reason = models.CharField(max_length=255)
    flagged_at = models.DateTimeField(auto_now_add=True)
    reviewed = models.BooleanField(default=False)

    def __str__(self):
        return f"Flagged by {self.user.username} for {self.reason}"
