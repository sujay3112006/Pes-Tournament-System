"""Matches App URLs"""
from django.urls import path
from apps.matches.views import (
    TournamentMatchesView,
    MatchDetailView,
    SubmitMatchResultView,
    UpdateMatchResultView,
    UserMatchStatsView,
    PlayerMatchesView,
)

urlpatterns = [
    # Match CRUD
    path('tournaments/<str:tournament_id>/matches/', TournamentMatchesView.as_view(), name='tournament_matches'),
    path('matches/<str:match_id>/', MatchDetailView.as_view(), name='match_detail'),
    
    # Submit and update results
    path('matches/<str:match_id>/submit-result/', SubmitMatchResultView.as_view(), name='submit_match_result'),
    path('matches/<str:match_id>/update-result/', UpdateMatchResultView.as_view(), name='update_match_result'),
    
    # Stats
    path('matches/stats/<str:user_id>/', UserMatchStatsView.as_view(), name='user_match_stats'),
    path('players/<str:user_id>/matches/', PlayerMatchesView.as_view(), name='player_matches'),
]
