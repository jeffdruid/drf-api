from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import FlaggedContent
from .serializers import FlaggedContentSerializer

class FlaggedContentViewSet(viewsets.ModelViewSet):
    queryset = FlaggedContent.objects.all()
    serializer_class = FlaggedContentSerializer

    def list(self, request, *args, **kwargs):
        flagged_content = FlaggedContent.objects.all()

        if not flagged_content.exists():
            # Custom response when no content is found
            return Response({'message': 'Connected: No flagged content found'}, status=status.HTTP_200_OK)

        serializer = self.get_serializer(flagged_content, many=True)
        return Response(serializer.data)
