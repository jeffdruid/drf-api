from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FlaggedContentViewSet, TriggerWordViewSet
from moderation import views as moderation_views

router = DefaultRouter()
router.register(r'flagged-content', moderation_views.FlaggedContentViewSet, basename='flaggedcontent')
router.register(r'triggerwords', moderation_views.TriggerWordViewSet, basename='triggerword')

urlpatterns = [
    path('', include(router.urls)),
]
