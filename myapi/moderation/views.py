from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import FlaggedContent
from .serializers import FlaggedContentSerializer

class FlaggedContentViewSet(viewsets.ModelViewSet):
    queryset = FlaggedContent.objects.all()
    serializer_class = FlaggedContentSerializer

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
