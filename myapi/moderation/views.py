from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import FlaggedContent, TriggerWord
from .serializers import FlaggedContentSerializer, TriggerWordSerializer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
import firebase_admin
from firebase_admin import firestore

# Initialize Firestore (make sure to configure Firebase Admin SDK)
if not firebase_admin._apps:
    firebase_admin.initialize_app()


class FlaggedContentViewSet(viewsets.ModelViewSet):
    queryset = FlaggedContent.objects.all()
    serializer_class = FlaggedContentSerializer

    def create(self, request, *args, **kwargs):
        try:
            # Log incoming request data
            print("Received flagged content:", request.data)

            # Get parent type and set required fields
            parent_type = request.data.get("parent_type", "post")
            required_fields = ["content", "reason", "user"]

            # Ensure required fields based on parent_type
            if parent_type == "post":
                required_fields.append("post_id")
            elif parent_type == "comment":
                required_fields.extend(["post_id", "comment_id"])
            elif parent_type == "reply":
                required_fields.extend(["post_id", "comment_id", "reply_id"])
            else:
                raise ValueError("Invalid parent_type specified.")

            # Check for missing fields
            for field in required_fields:
                if field not in request.data:
                    raise ValueError(
                        f"'{field}' is a required field for {parent_type}."
                    )

            # Create flagged content instance
            flagged_content = FlaggedContent.objects.create(
                post_id=request.data.get("post_id"),
                content=request.data["content"],
                reason=request.data["reason"],
                user=request.data["user"],
                comment_id=request.data.get("comment_id"),
                reply_id=request.data.get("reply_id"),
            )
            return Response({"success": True}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print("Error in create:", e)
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = {
            "reviewed": request.data.get("reviewed", instance.reviewed),
            "is_visible": request.data.get("is_visible", instance.is_visible),
        }
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Firestore update logic
        try:
            db = firestore.client()

            # Determine Firestore path based on available IDs in the instance
            if instance.reply_id:
                # If it's a reply
                doc_ref = (
                    db.collection("Posts")
                    .document(instance.post_id)
                    .collection("Comments")
                    .document(instance.comment_id)
                    .collection("Replies")
                    .document(instance.reply_id)
                )
            elif instance.comment_id:
                # If it's a comment
                doc_ref = (
                    db.collection("Posts")
                    .document(instance.post_id)
                    .collection("Comments")
                    .document(instance.comment_id)
                )
            else:
                # If it's a post
                doc_ref = db.collection("Posts").document(instance.post_id)

            # Update Firestore document visibility and review status
            doc_ref.update(
                {
                    "is_visible": data["is_visible"],
                    "reviewed": data["reviewed"],
                }
            )
            print(
                f"Firestore document updated successfully at path: "
                f"{doc_ref.path}"
            )

        except Exception as e:
            print(f"Error updating Firestore for ID {instance.id}: {e}")
            return Response(
                {"error": f"Firestore update failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(serializer.data, status=status.HTTP_200_OK)

    # Action to check for trigger words
    @action(detail=False, methods=["post"], url_path="check")
    def check_content(self, request):
        content = request.data.get("content", "")
        trigger_words = TriggerWord.objects.values_list("word", flat=True)
        flagged = any(word in content.lower() for word in trigger_words)

        if flagged:
            return Response(
                {"flagged": True, "message": "Content contains trigger words."}
            )

        return Response({"flagged": False}, status=status.HTTP_200_OK)


class TriggerWordViewSet(viewsets.ModelViewSet):
    queryset = TriggerWord.objects.all()
    serializer_class = TriggerWordSerializer
    permission_classes = [
        IsAuthenticated
    ]  # Ensures only authenticated users can access

    @action(detail=False, methods=["post"], url_path="check")
    def check_content(self, request):
        content = request.data.get("content", "")
        trigger_words = TriggerWord.objects.values_list("word", flat=True)
        flagged = any(word in content.lower() for word in trigger_words)

        if flagged:
            return Response(
                {"flagged": True, "message": "Content contains trigger words."}
            )

        return Response({"flagged": False}, status=status.HTTP_200_OK)
