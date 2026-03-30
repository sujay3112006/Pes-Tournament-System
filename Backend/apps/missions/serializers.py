"""Missions App Serializers"""
from rest_framework import serializers


class MissionSerializer(serializers.Serializer):
    """Mission serializer."""
    mission_id = serializers.CharField(read_only=True)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    mission_type = serializers.ChoiceField(choices=['daily', 'weekly', 'seasonal', 'special'])
    reward_points = serializers.IntegerField()
    difficulty = serializers.ChoiceField(choices=['easy', 'medium', 'hard', 'expert'])
    status = serializers.ChoiceField(choices=['active', 'inactive', 'completed'])


class UserMissionSerializer(serializers.Serializer):
    """User mission serializer."""
    user_mission_id = serializers.CharField(read_only=True)
    user_id = serializers.CharField()
    mission_id = serializers.CharField()
    mission_title = serializers.CharField(read_only=True)
    progress = serializers.IntegerField()
    completed = serializers.BooleanField(read_only=True)
    claimed = serializers.BooleanField()
