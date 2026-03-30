"""Tournaments App Serializers"""
from rest_framework import serializers
from apps.tournaments.models import Tournament, TournamentPlayer
from django.utils import timezone


class TournamentCreateSerializer(serializers.Serializer):
    """Serializer for creating tournaments."""
    name = serializers.CharField(max_length=255, required=True)
    description = serializers.CharField(max_length=1000, required=False, allow_blank=True)
    format = serializers.ChoiceField(choices=['Knockout', 'League'], required=True)
    max_players = serializers.IntegerField(min_value=2, max_value=128, default=16)
    start_date = serializers.DateTimeField(required=True)
    end_date = serializers.DateTimeField(required=True)
    location = serializers.CharField(max_length=255, required=False, allow_blank=True)
    rules = serializers.CharField(max_length=2000, required=False, allow_blank=True)
    prize_pool = serializers.IntegerField(min_value=0, default=0)
    is_public = serializers.BooleanField(default=True)
    
    def validate(self, data):
        """Validate tournament dates."""
        if data['start_date'] <= timezone.now():
            raise serializers.ValidationError(
                {'start_date': 'Tournament start date must be in the future.'}
            )
        if data['end_date'] <= data['start_date']:
            raise serializers.ValidationError(
                {'end_date': 'Tournament end date must be after start date.'}
            )
        return data


class TournamentPlayerSerializer(serializers.Serializer):
    """Serializer for tournament players."""
    tournament_player_id = serializers.CharField(read_only=True)
    user_id = serializers.CharField(read_only=True)
    username = serializers.CharField(read_only=True)
    joined_at = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(read_only=True)
    points = serializers.IntegerField(read_only=True)
    matches_played = serializers.IntegerField(read_only=True)
    wins = serializers.IntegerField(read_only=True)
    losses = serializers.IntegerField(read_only=True)
    draws = serializers.IntegerField(read_only=True)


class TournamentListSerializer(serializers.Serializer):
    """Serializer for listing tournaments."""
    tournament_id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    creator_id = serializers.CharField(read_only=True)
    format = serializers.CharField(read_only=True)
    max_players = serializers.IntegerField(read_only=True)
    current_players = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)
    start_date = serializers.DateTimeField(read_only=True)
    end_date = serializers.DateTimeField(read_only=True)
    is_public = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)


class TournamentDetailSerializer(serializers.Serializer):
    """Serializer for tournament details."""
    tournament_id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    creator_id = serializers.CharField(read_only=True)
    format = serializers.CharField(read_only=True)
    max_players = serializers.IntegerField(read_only=True)
    current_players = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)
    start_date = serializers.DateTimeField(read_only=True)
    end_date = serializers.DateTimeField(read_only=True)
    location = serializers.CharField(read_only=True)
    rules = serializers.CharField(read_only=True)
    prize_pool = serializers.IntegerField(read_only=True)
    is_public = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    players = TournamentPlayerSerializer(many=True, read_only=True)


class JoinTournamentSerializer(serializers.Serializer):
    """Serializer for joining a tournament."""
    pass  # No additional fields needed, user_id comes from request


class TournamentUpdateSerializer(serializers.Serializer):
    """Serializer for updating tournament (admin only)."""
    description = serializers.CharField(max_length=1000, required=False, allow_blank=True)
    location = serializers.CharField(max_length=255, required=False, allow_blank=True)
    rules = serializers.CharField(max_length=2000, required=False, allow_blank=True)
    status = serializers.ChoiceField(
        choices=['draft', 'registration', 'active', 'completed', 'cancelled'],
        required=False
    )
