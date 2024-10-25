from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import FlaggedContent
from .serializers import FlaggedContentSerializer
from rest_framework.decorators import action

class FlaggedContentViewSet(viewsets.ModelViewSet):
    queryset = FlaggedContent.objects.all()
    serializer_class = FlaggedContentSerializer
    
     # Custom action for checking content without saving flagged content
    @action(detail=False, methods=['post'], url_path='check')
    def check_content(self, request):
        content = request.data.get('content', '')
        
        # Simple trigger word example
        trigger_words = [
            # Suicide-related
            "suicide", "suicidal", "kill myself", "kms", "k/ys", "kys", "end my life", "take my life", 
            "hang myself", "overdose", "OD", "CO", "SW", "RIP", "x_x", "88", "CTB", "catch the bus", 
            "deep sleep", "permanent solution", "exit plan", "final exit", "punch out", "long nap", 
            "peaceful pill", "golden gate", "rope", "helium hood", "blackout method",
            
            # Self-harm-related
            "self-harm", "SI", "SH", "C/S", "cut myself", "cutting", "slit wrists", "hurt myself", 
            "burn myself", "scar myself", "self-injury", "bleed out", "razor", "slicing", "red bracelet", 
            "scratching", "carving", "blade", "hurting", "hurting oneself", "pinky promise",
        ]
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
