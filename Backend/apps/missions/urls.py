"""Missions App URLs"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.missions.views import MissionViewSet, UserMissionViewSet

router = DefaultRouter()
router.register(r'missions', MissionViewSet, basename='mission')
router.register(r'user-missions', UserMissionViewSet, basename='user-mission')

urlpatterns = [
    path('', include(router.urls)),
]
