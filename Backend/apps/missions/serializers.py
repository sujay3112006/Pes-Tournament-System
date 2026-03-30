"""Missions App Serializers"""
from rest_framework import serializers
from apps.missions.models import Mission, UserMission
from django.utils import timezone


class MissionRewardSerializer(serializers.Serializer):
    """Serializer for mission rewards."""
    coins = serializers.IntegerField(required=False, min_value=0)
    points = serializers.IntegerField(required=False, min_value=0)
    badge_id = serializers.CharField(required=False, allow_null=True)
    item_id = serializers.CharField(required=False, allow_null=True)


class MissionConditionSerializer(serializers.Serializer):
    """Serializer for mission conditions."""
    condition_type = serializers.CharField(required=True)
    value = serializers.IntegerField(required=True, min_value=1)


class MissionSerializer(serializers.Serializer):
    """Serializer for available missions."""
    mission_id = serializers.CharField(read_only=True)
    title = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    mission_type = serializers.CharField(read_only=True)
    difficulty = serializers.CharField(read_only=True)
    reward = MissionRewardSerializer(read_only=True)
    condition = MissionConditionSerializer(read_only=True)
    status = serializers.CharField(read_only=True)
    start_date = serializers.DateTimeField(read_only=True)
    end_date = serializers.DateTimeField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)


class UserMissionSerializer(serializers.Serializer):
    """Serializer for user mission progress."""
    user_mission_id = serializers.CharField(read_only=True)
    mission_id = serializers.CharField(read_only=True)
    mission_title = serializers.CharField(read_only=True)
    progress = serializers.IntegerField(read_only=True)
    condition_value = serializers.IntegerField(read_only=True)
    progress_percentage = serializers.SerializerMethodField(read_only=True)
    completed = serializers.BooleanField(read_only=True)
    completed_at = serializers.DateTimeField(read_only=True, allow_null=True)
    reward_claimed = serializers.BooleanField(read_only=True)
    claimed_at = serializers.DateTimeField(read_only=True, allow_null=True)
    started_at = serializers.DateTimeField(read_only=True)
    
    def get_progress_percentage(self, obj):
        """Calculate progress percentage."""
        if obj.condition_value == 0:
            return 0
        return round((obj.progress / obj.condition_value) * 100, 2)


class UserMissionDetailSerializer(serializers.Serializer):
    """Serializer for detailed user mission view."""
    user_mission_id = serializers.CharField(read_only=True)
    mission_id = serializers.CharField(read_only=True)
    mission_title = serializers.CharField(read_only=True)
    mission_description = serializers.CharField(read_only=True)
    mission_type = serializers.CharField(read_only=True)
    difficulty = serializers.CharField(read_only=True)
    progress = serializers.IntegerField(read_only=True)
    condition_value = serializers.IntegerField(read_only=True)
    progress_percentage = serializers.SerializerMethodField(read_only=True)
    completed = serializers.BooleanField(read_only=True)
    completed_at = serializers.DateTimeField(read_only=True, allow_null=True)
    reward = MissionRewardSerializer(read_only=True)
    reward_claimed = serializers.BooleanField(read_only=True)
    claimed_at = serializers.DateTimeField(read_only=True, allow_null=True)
    started_at = serializers.DateTimeField(read_only=True)
    
    def get_progress_percentage(self, obj):
        """Calculate progress percentage."""
        if obj.condition_value == 0:
            return 0
        return round((obj.progress / obj.condition_value) * 100, 2)


class UpdateMissionProgressSerializer(serializers.Serializer):
    """Serializer for updating mission progress."""
    progress_increment = serializers.IntegerField(required=True, min_value=1)


class ClaimRewardSerializer(serializers.Serializer):
    """Serializer for claiming mission rewards."""
    mission_id = serializers.CharField(required=True)


class MissionStatsSerializer(serializers.Serializer):
    """Serializer for mission statistics."""
    total_missions = serializers.IntegerField()
    completed_missions = serializers.IntegerField()
    active_missions = serializers.IntegerField()
    pending_rewards = serializers.IntegerField()
    total_coins_from_missions = serializers.IntegerField()
    total_points_from_missions = serializers.IntegerField()


class CompletedMissionSerializer(serializers.Serializer):
    """Serializer for completed but unclaimed missions."""
    user_mission_id = serializers.CharField(read_only=True)
    mission_id = serializers.CharField(read_only=True)
    mission_title = serializers.CharField(read_only=True)
    difficulty = serializers.CharField(read_only=True)
    reward = MissionRewardSerializer(read_only=True)
    completed_at = serializers.DateTimeField(read_only=True)


class MissionProgressUpdateResponseSerializer(serializers.Serializer):
    """Serializer for mission progress update response."""
    message = serializers.CharField(read_only=True)
    progress = serializers.IntegerField(read_only=True)
    condition_value = serializers.IntegerField(read_only=True)
    progress_percentage = serializers.FloatField(read_only=True)
    completed = serializers.BooleanField(read_only=True)
    can_claim_reward = serializers.BooleanField(read_only=True)
