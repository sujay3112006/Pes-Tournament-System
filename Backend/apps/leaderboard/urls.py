"""Leaderboard App URLs"""
from django.urls import path
from apps.leaderboard.views import (
    TournamentLeaderboardView,
    TopPlayersView,
    PlayerLeaderboardStatsView,
    PlayerRankComparisonView,
    UpdateMatchResultView,
    RankedPlayerListView,
)

urlpatterns = [
    # Leaderboard retrieval
    path('tournaments/<str:tournament_id>/leaderboard/', TournamentLeaderboardView.as_view(), name='tournament_leaderboard'),
    path('tournaments/<str:tournament_id>/rankings/', RankedPlayerListView.as_view(), name='ranked_players'),
    path('tournaments/<str:tournament_id>/top-players/', TopPlayersView.as_view(), name='top_players'),
    
    # Player stats
    path('tournaments/<str:tournament_id>/players/<str:user_id>/stats/', PlayerLeaderboardStatsView.as_view(), name='player_leaderboard_stats'),
    path('tournaments/<str:tournament_id>/players/my-rank/', PlayerRankComparisonView.as_view(), name='my_rank_comparison'),
    
    # Update points
    path('leaderboard/update-match-result/', UpdateMatchResultView.as_view(), name='update_match_result'),
]
