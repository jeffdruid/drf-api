from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import FlaggedContent
from .serializers import FlaggedContentSerializer

# Trigger words list including slang, code words, and abbreviations
TRIGGER_WORDS = [
    # Suicide-related
    "suicide", "suicidal", "kill myself", "kms", "k/ys", "kys", "end my life", "take my life", 
    "hang myself", "overdose", "OD", "CO", "SW", "RIP", "x_x", "88", "CTB", "catch the bus", 
    "deep sleep", "permanent solution", "exit plan", "final exit", "punch out", "long nap", 
    "peaceful pill", "golden gate", "rope", "helium hood", "blackout method",
    
    # Self-harm-related
    "self-harm", "SI", "SH", "C/S", "cut myself", "cutting", "slit wrists", "hurt myself", 
    "burn myself", "scar myself", "self-injury", "bleed out", "razor", "slicing", "red bracelet", 
    "scratching", "carving", "blade", "hurting", "hurting oneself", "pinky promise",

    # Depression and Distress-related
    "depression", "empty", "hollow", "hopeless", "worthless", "FML", "TFW", "black dog", "numb", 
    "dead inside", "I'm done", "can't deal", "at the end", "low", "trapped", "nobody cares", 
    "suffocate", "over it", "drowning", "zoned out", "EOD", "no way out", "mentally gone", 
    "DGAF", "SAD"
]

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
