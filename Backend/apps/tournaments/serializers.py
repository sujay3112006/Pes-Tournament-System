"""Tournaments App Serializers"""
from rest_framework import serializers


class TournamentSerializer(serializers.Serializer):
    """Tournament serializer."""
    tournament_id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False)
    creator_id = serializers.CharField()
    banner_image = serializers.URLField(required=False)
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    total_teams = serializers.IntegerField(read_only=True)
    status = serializers.ChoiceField(choices=['draft', 'active', 'completed', 'cancelled'])
    tournament_type = serializers.ChoiceField(choices=['league', 'knockout', 'group', 'round_robin'])
    max_teams = serializers.IntegerField()
    rules = serializers.CharField(required=False)
    prize_pool = serializers.CharField()
    location = serializers.CharField(required=False)
    is_public = serializers.BooleanField()
    created_at = serializers.DateTimeField(read_only=True)


class TournamentTeamSerializer(serializers.Serializer):
    """Tournament team serializer."""
    tournament_id = serializers.CharField(read_only=True)
    team_id = serializers.CharField()
    team_name = serializers.CharField()
    captain_id = serializers.CharField()
    members = serializers.ListField(child=serializers.CharField())
    status = serializers.ChoiceField(choices=['active', 'eliminated', 'withdrawn'])
    points = serializers.IntegerField(read_only=True)
    matches_played = serializers.IntegerField(read_only=True)
    wins = serializers.IntegerField(read_only=True)
    draws = serializers.IntegerField(read_only=True)
    losses = serializers.IntegerField(read_only=True)
