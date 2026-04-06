"""Leaderboard App URLs"""
from django.urls import path
from apps.leaderboard.views import (
    TournamentLeaderboardView,
    TopPlayersView,
    PlayerLeaderboardStatsView,
    PlayerRankComparisonView,
    UpdateMatchResultView,
    RankedPlayerListView,
    GlobalTopPlayersView,
    GlobalRankingsView,
    GlobalPlayerStatsView,
)

urlpatterns = [
    # Global leaderboard (no tournament required)
    path('top-players/', GlobalTopPlayersView.as_view(), name='global_top_players'),
    path('rankings/', GlobalRankingsView.as_view(), name='global_rankings'),
    path('player/<str:user_id>/stats/', GlobalPlayerStatsView.as_view(), name='global_player_stats'),
    
    # Leaderboard retrieval (tournament-specific)
    path('tournament/<str:tournament_id>/', TournamentLeaderboardView.as_view(), name='tournament_leaderboard'),
    path('tournament/<str:tournament_id>/rankings/', RankedPlayerListView.as_view(), name='ranked_players'),
    path('tournament/<str:tournament_id>/top-players/', TopPlayersView.as_view(), name='top_players'),
    
    # Player stats (tournament-specific)
    path('tournament/<str:tournament_id>/player/<str:user_id>/stats/', PlayerLeaderboardStatsView.as_view(), name='player_leaderboard_stats'),
    path('tournament/<str:tournament_id>/player/my-rank/', PlayerRankComparisonView.as_view(), name='my_rank_comparison'),
    
    # Update points
    path('update-match-result/', UpdateMatchResultView.as_view(), name='update_match_result'),
]
