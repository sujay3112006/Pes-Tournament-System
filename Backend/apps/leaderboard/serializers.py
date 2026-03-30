"""Leaderboard App Serializers"""
from rest_framework import serializers
from apps.leaderboard.models import Leaderboard, LeaderboardEntry


class LeaderboardEntrySerializer(serializers.Serializer):
    """Serializer for leaderboard entry."""
    entry_id = serializers.CharField(read_only=True)
    tournament_id = serializers.CharField(read_only=True)
    user_id = serializers.CharField(read_only=True)
    username = serializers.CharField(read_only=True)
    rank = serializers.IntegerField(read_only=True)
    points = serializers.IntegerField(read_only=True)
    matches_played = serializers.IntegerField(read_only=True)
    wins = serializers.IntegerField(read_only=True)
    losses = serializers.IntegerField(read_only=True)
    draws = serializers.IntegerField(read_only=True)
    goal_difference = serializers.IntegerField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class LeaderboardSerializer(serializers.Serializer):
    """Serializer for leaderboard view."""
    leaderboard_id = serializers.CharField(read_only=True)
    tournament_id = serializers.CharField(read_only=True)
    total_entries = serializers.IntegerField(read_only=True)
    entries = LeaderboardEntrySerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class RankingListSerializer(serializers.Serializer):
    """Serializer for compact ranking list."""
    rank = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    user_id = serializers.CharField(read_only=True)
    points = serializers.IntegerField(read_only=True)
    matches_played = serializers.IntegerField(read_only=True)
    wins = serializers.IntegerField(read_only=True)
    losses = serializers.IntegerField(read_only=True)
    draws = serializers.IntegerField(read_only=True)
    win_rate = serializers.SerializerMethodField(read_only=True)
    
    def get_win_rate(self, obj):
        """Calculate win rate percentage."""
        if obj.matches_played == 0:
            return 0
        return round((obj.wins / obj.matches_played) * 100, 2)


class UpdateMatchResultSerializer(serializers.Serializer):
    """Serializer for updating match result in leaderboard."""
    match_id = serializers.CharField(required=True)
    tournament_id = serializers.CharField(required=True)
    player1_id = serializers.CharField(required=True)
    player2_id = serializers.CharField(required=True)
    player1_score = serializers.IntegerField(required=True, min_value=0)
    player2_score = serializers.IntegerField(required=True, min_value=0)
    winner_id = serializers.CharField(required=False, allow_null=True)


class PlayerLeaderboardStatsSerializer(serializers.Serializer):
    """Serializer for player's leaderboard statistics."""
    user_id = serializers.CharField(read_only=True)
    username = serializers.CharField(read_only=True)
    tournament_id = serializers.CharField(read_only=True)
    rank = serializers.IntegerField(read_only=True)
    points = serializers.IntegerField(read_only=True)
    matches_played = serializers.IntegerField(read_only=True)
    wins = serializers.IntegerField(read_only=True)
    losses = serializers.IntegerField(read_only=True)
    draws = serializers.IntegerField(read_only=True)
    win_rate = serializers.SerializerMethodField(read_only=True)
    goal_difference = serializers.IntegerField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    def get_win_rate(self, obj):
        """Calculate win rate percentage."""
        if obj.matches_played == 0:
            return 0
        return round((obj.wins / obj.matches_played) * 100, 2)


class LeaderboardComparisonSerializer(serializers.Serializer):
    """Serializer for comparing player to leaderboard."""
    user_id = serializers.CharField(read_only=True)
    username = serializers.CharField(read_only=True)
    rank = serializers.IntegerField(read_only=True)
    points = serializers.IntegerField(read_only=True)
    rank_change = serializers.IntegerField(read_only=True, allow_null=True)
    points_to_next = serializers.IntegerField(read_only=True, allow_null=True)
    percentage_to_first = serializers.SerializerMethodField(read_only=True)
    
    def get_percentage_to_first(self, obj):
        """Calculate percentage toward first place."""
        # This would be calculated in the view
        return obj.__dict__.get('percentage_to_first', 0)


class TopPlayersSerializer(serializers.Serializer):
    """Serializer for top N players."""
    rank = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    user_id = serializers.CharField(read_only=True)
    points = serializers.IntegerField(read_only=True)
    matches_played = serializers.IntegerField(read_only=True)
    wins = serializers.IntegerField(read_only=True)
