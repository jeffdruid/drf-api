from rest_framework import serializers
from .models import FlaggedContent, TriggerWord

class FlaggedContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlaggedContent
        fields = ['user', 'post_id', 'reason', 'flagged_at', 'reviewed', 'content']

class TriggerWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = TriggerWord
        fields = ['id', 'word', 'category', 'created_at', 'updated_at']
