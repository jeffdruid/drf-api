from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source="owner.profile.id")
    profile_image = serializers.ReadOnlyField(source="owner.profile.image.url")
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "owner",
            "is_owner",
            "profile_id",
            "profile_image",
            "post",
            "created_at",
            "updated_at",
            "content",
        ]

    def get_is_owner(self, obj):
        request = self.context.get("request")
        if request:
            return obj.owner == request.user
        return False

    def get_created_at(self, obj):
        return naturaltime(obj.created_at)

    def get_updated_at(self, obj):
        return naturaltime(obj.updated_at)


class CommentDetailSerializer(CommentSerializer):
    post = serializers.ReadOnlyField(source="post.id")

    class Meta(CommentSerializer.Meta):
        fields = CommentSerializer.Meta.fields + ["post"]
