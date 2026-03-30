"""Matches App Serializers"""
from rest_framework import serializers


class MatchSerializer(serializers.Serializer):
    """Match serializer."""
    match_id = serializers.CharField(read_only=True)
    tournament_id = serializers.CharField()
    team_a_id = serializers.CharField()
    team_b_id = serializers.CharField()
    team_a_name = serializers.CharField()
    team_b_name = serializers.CharField()
    match_date = serializers.DateTimeField()
    status = serializers.ChoiceField(choices=['scheduled', 'live', 'completed', 'cancelled'])
    team_a_score = serializers.IntegerField(read_only=True)
    team_b_score = serializers.IntegerField(read_only=True)
    winner_id = serializers.CharField(read_only=True)
    location = serializers.CharField(required=False)


class MatchEventSerializer(serializers.Serializer):
    """Match event serializer."""
    match_id = serializers.CharField()
    event_type = serializers.ChoiceField(choices=['goal', 'yellow_card', 'red_card', 'substitution', 'own_goal'])
    player_id = serializers.CharField()
    team_id = serializers.CharField()
    minute = serializers.IntegerField()
    description = serializers.CharField(required=False)
