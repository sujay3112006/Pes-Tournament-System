"""Clubs App Serializers"""
from rest_framework import serializers


class ClubSerializer(serializers.Serializer):
    """Club serializer."""
    club_id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    logo_url = serializers.URLField(required=False)
    owner_id = serializers.CharField()
    member_count = serializers.IntegerField(read_only=True)
    is_verified = serializers.BooleanField()
    total_tournaments = serializers.IntegerField(read_only=True)
    total_wins = serializers.IntegerField(read_only=True)


class ClubMemberSerializer(serializers.Serializer):
    """Club member serializer."""
    member_id = serializers.CharField(read_only=True)
    club_id = serializers.CharField()
    user_id = serializers.CharField()
    username = serializers.CharField()
    role = serializers.ChoiceField(choices=['owner', 'admin', 'member'])
    joined_at = serializers.DateTimeField(read_only=True)
