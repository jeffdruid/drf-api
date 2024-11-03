from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import FlaggedContent, TriggerWord
from .serializers import FlaggedContentSerializer, TriggerWordSerializer
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated


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
