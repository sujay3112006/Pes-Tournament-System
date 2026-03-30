"""Matches App Serializers"""
from rest_framework import serializers
from apps.matches.models import Match, MatchEvent
from django.core.files.storage import default_storage
import os


class MatchEventSerializer(serializers.Serializer):
    """Match event serializer."""
    event_id = serializers.CharField(read_only=True)
    event_type = serializers.CharField(read_only=True)
    player_id = serializers.CharField(read_only=True)
    minute = serializers.IntegerField(read_only=True)
    description = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)


class MatchListSerializer(serializers.Serializer):
    """Serializer for listing matches."""
    match_id = serializers.CharField(read_only=True)
    tournament_id = serializers.CharField(read_only=True)
    player1_username = serializers.CharField(read_only=True)
    player2_username = serializers.CharField(read_only=True)
    match_date = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(read_only=True)
    score = serializers.JSONField(read_only=True)
    winner_id = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)


class MatchDetailSerializer(serializers.Serializer):
    """Serializer for match details."""
    match_id = serializers.CharField(read_only=True)
    tournament_id = serializers.CharField(read_only=True)
    player1_id = serializers.CharField(read_only=True)
    player2_id = serializers.CharField(read_only=True)
    player1_username = serializers.CharField(read_only=True)
    player2_username = serializers.CharField(read_only=True)
    match_date = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(read_only=True)
    score = serializers.JSONField(read_only=True)
    winner_id = serializers.CharField(read_only=True, allow_null=True)
    location = serializers.CharField(read_only=True)
    proof_url = serializers.URLField(read_only=True, allow_null=True)
    duration = serializers.IntegerField(read_only=True, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    events = MatchEventSerializer(many=True, read_only=True)


class SubmitMatchResultSerializer(serializers.Serializer):
    """Serializer for submitting match results."""
    player1_score = serializers.IntegerField(min_value=0, required=True)
    player2_score = serializers.IntegerField(min_value=0, required=True)
    proof = serializers.FileField(required=False, allow_null=True)
    location = serializers.CharField(max_length=255, required=False, allow_blank=True)
    duration = serializers.IntegerField(min_value=1, required=False, allow_null=True)
    notes = serializers.CharField(max_length=500, required=False, allow_blank=True)
    
    def validate_proof(self, value):
        """Validate proof file."""
        if value:
            # Check file size (max 10MB)
            if value.size > 10 * 1024 * 1024:
                raise serializers.ValidationError("File size cannot exceed 10MB.")
            
            # Check file type
            allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'pdf', 'mp4', 'mov']
            file_ext = value.name.split('.')[-1].lower()
            if file_ext not in allowed_extensions:
                raise serializers.ValidationError(
                    f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
                )
        
        return value


class UpdateMatchResultSerializer(serializers.Serializer):
    """Serializer for updating match results."""
    player1_score = serializers.IntegerField(min_value=0, required=False)
    player2_score = serializers.IntegerField(min_value=0, required=False)
    proof = serializers.FileField(required=False, allow_null=True)
    status = serializers.ChoiceField(
        choices=['scheduled', 'live', 'completed', 'cancelled', 'disputed'],
        required=False
    )
    duration = serializers.IntegerField(min_value=1, required=False, allow_null=True)
    notes = serializers.CharField(max_length=500, required=False, allow_blank=True)
    
    def validate_proof(self, value):
        """Validate proof file."""
        if value:
            # Check file size (max 10MB)
            if value.size > 10 * 1024 * 1024:
                raise serializers.ValidationError("File size cannot exceed 10MB.")
            
            # Check file type
            allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'pdf', 'mp4', 'mov']
            file_ext = value.name.split('.')[-1].lower()
            if file_ext not in allowed_extensions:
                raise serializers.ValidationError(
                    f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
                )
        
        return value


class MatchStatsSerializer(serializers.Serializer):
    """Serializer for match statistics."""
    total_matches = serializers.IntegerField()
    completed_matches = serializers.IntegerField()
    pending_matches = serializers.IntegerField()
    wins = serializers.IntegerField()
    losses = serializers.IntegerField()
    draws = serializers.IntegerField()
