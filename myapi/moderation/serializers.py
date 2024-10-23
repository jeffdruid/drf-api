from rest_framework import serializers
from .models import FlaggedContent

class FlaggedContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlaggedContent
        fields = ['user', 'post_id', 'reason', 'flagged_at', 'reviewed']
