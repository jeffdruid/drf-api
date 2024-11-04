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
    
    # Custom action for checking content without saving flagged content
    @action(detail=False, methods=['post'], url_path='check')
    def check_content(self, request):
        content = request.data.get('content', '')
        
        # Fetch all trigger words from the database
        trigger_words = TriggerWord.objects.values_list('word', flat=True)
        flagged = any(word in content.lower() for word in trigger_words)
        
        if flagged:
            return Response({"flagged": True, "message": "Content contains trigger words."})
        
        return Response({"flagged": False}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        try:
            # Log the incoming request data
            print(request.data)

            # Validate required fields
            required_fields = ['post_id', 'content', 'reason', 'user']
            for field in required_fields:
                if field not in request.data:
                    raise ValueError(f"'{field}' is a required field.")

            flagged_content = FlaggedContent.objects.create(
                post_id=request.data.get('post_id'),
                content=request.data['content'],
                reason=request.data['reason'],
                user=request.data['user'],  # Ensure this matches the 'user' field
            )
            return Response({"success": True}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            print(e)  # Check the exact error in the console
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
            doc_ref = db.collection('Posts').document(instance.post_id)
            doc_ref.update({
                'is_visible': data['is_visible'],
                'reviewed': data['reviewed']
            })
            print("Firestore document updated successfully.")
        except Exception as e:
            print(f"Error updating Firestore: {e}")
            return Response({"error": f"Firestore update failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.data, status=status.HTTP_200_OK)

class TriggerWordViewSet(viewsets.ModelViewSet):
    queryset = TriggerWord.objects.all()
    serializer_class = TriggerWordSerializer
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access

    @action(detail=False, methods=['post'], url_path='check')
    def check_content(self, request):
        content = request.data.get('content', '')
        trigger_words = TriggerWord.objects.values_list('word', flat=True)
        flagged = any(word in content.lower() for word in trigger_words)
        
        if flagged:
            return Response({"flagged": True, "message": "Content contains trigger words."})
        
        return Response({"flagged": False}, status=status.HTTP_200_OK)
