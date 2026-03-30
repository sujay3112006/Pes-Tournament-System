"""Clubs App URLs"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.clubs.views import ClubViewSet, ClubMemberViewSet

router = DefaultRouter()
router.register(r'clubs', ClubViewSet, basename='club')
router.register(r'members', ClubMemberViewSet, basename='club-member')

urlpatterns = [
    path('', include(router.urls)),
]
