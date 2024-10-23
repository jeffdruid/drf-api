from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FlaggedContentViewSet

router = DefaultRouter()
router.register(r'flagged-content', FlaggedContentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
