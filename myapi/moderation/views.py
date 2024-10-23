from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import FlaggedContent
from .serializers import FlaggedContentSerializer

# Trigger words list
TRIGGER_WORDS = ["distress", "depression", "anxiety", "suicide"]

def check_trigger_words(content):
    for word in TRIGGER_WORDS:
        if word in content.lower():
            return True
    return False

class FlaggedContentViewSet(viewsets.ModelViewSet):
    queryset = FlaggedContent.objects.all()
    serializer_class = FlaggedContentSerializer

    def create(self, request, *args, **kwargs):
        content = request.data.get('content', '')
        if check_trigger_words(content):
            return Response({"flagged": True, "message": "Content contains trigger words"}, status=status.HTTP_200_OK)
        return Response({"flagged": False, "message": "Content is safe"}, status=status.HTTP_200_OK)
