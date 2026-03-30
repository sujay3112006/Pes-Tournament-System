"""Matches App URLs"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.matches.views import MatchViewSet, MatchEventViewSet

router = DefaultRouter()
router.register(r'list', MatchViewSet, basename='match')
router.register(r'events', MatchEventViewSet, basename='match-event')

urlpatterns = [
    path('', include(router.urls)),
]
