from django.db import models
from django.contrib.auth.models import User

class FlaggedContent(models.Model):
    post_id = models.CharField(max_length=100)  # Firebase post ID
    content = models.TextField()
    reason = models.CharField(max_length=255)
    user = models.CharField(max_length=255)  # Firebase user UID
    flagged_at = models.DateTimeField(auto_now_add=True)
    reviewed = models.BooleanField(default=False)


    def __str__(self):
        return f"Flagged by {self.user} for {self.reason}"  # Remove .username since user is a CharField
