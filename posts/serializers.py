from rest_framework import serializers
from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source="owner.profile.id")
    profile_image = serializers.ReadOnlyField(source="owner.profile.image.url")

    def validate_image(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError("Image file too large ( > 2mb )")
        if value.image.width > 4096 or value.image.height > 4096:
            raise serializers.ValidationError(
                "Image width or height is too large"
            )
        return value

    class Meta:
        model = Post
        fields = ["__all__"]

    def get_is_owner(self, obj):
        request = self.context.get("request")
        return request.user == obj.owner