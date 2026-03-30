"""Tournaments App URLs"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.tournaments.views import TournamentViewSet, TournamentTeamViewSet

router = DefaultRouter()
router.register(r'tournaments', TournamentViewSet, basename='tournament')
router.register(r'teams', TournamentTeamViewSet, basename='tournament-team')

urlpatterns = [
    path('', include(router.urls)),
]
