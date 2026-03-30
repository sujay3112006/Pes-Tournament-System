"""Leaderboard App Serializers"""
from rest_framework import serializers


class LeaderboardEntrySerializer(serializers.Serializer):
    """Leaderboard entry serializer."""
    rank = serializers.IntegerField()
    team_id = serializers.CharField()
    team_name = serializers.CharField()
    points = serializers.IntegerField()
    matches_played = serializers.IntegerField()
    wins = serializers.IntegerField()
    draws = serializers.IntegerField()
    losses = serializers.IntegerField()
    goal_for = serializers.IntegerField()
    goal_against = serializers.IntegerField()
    goal_difference = serializers.IntegerField()
