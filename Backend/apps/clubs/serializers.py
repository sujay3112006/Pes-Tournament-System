"""Clubs App Serializers"""
from rest_framework import serializers
from apps.clubs.models import Club, ClubMember
from django.utils import timezone


class ClubMemberSerializer(serializers.Serializer):
    """Serializer for club member."""
    member_id = serializers.CharField(read_only=True)
    user_id = serializers.CharField(read_only=True)
    username = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)
    contribution_score = serializers.IntegerField(read_only=True)
    joined_at = serializers.DateTimeField(read_only=True)


class ClubListSerializer(serializers.Serializer):
    """Serializer for club listings."""
    club_id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    logo_url = serializers.URLField(read_only=True, allow_null=True)
    owner_username = serializers.CharField(read_only=True)
    member_count = serializers.IntegerField(read_only=True)
    total_tournaments = serializers.IntegerField(read_only=True)
    total_wins = serializers.IntegerField(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)
    founded_date = serializers.DateTimeField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)


class ClubDetailSerializer(serializers.Serializer):
    """Serializer for detailed club view."""
    club_id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    logo_url = serializers.URLField(read_only=True, allow_null=True)
    owner_id = serializers.CharField(read_only=True)
    owner_username = serializers.CharField(read_only=True)
    member_count = serializers.IntegerField(read_only=True)
    members_list = serializers.SerializerMethodField(read_only=True)
    total_tournaments = serializers.IntegerField(read_only=True)
    total_wins = serializers.IntegerField(read_only=True)
    stats = serializers.DictField(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)
    founded_date = serializers.DateTimeField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    def get_members_list(self, obj):
        """Get members with detailed info."""
        members = ClubMember.objects(club_id=obj.club_id).order_by('-joined_at')
        return ClubMemberSerializer(members, many=True).data


class CreateClubSerializer(serializers.Serializer):
    """Serializer for creating a club."""
    name = serializers.CharField(max_length=255, required=True)
    description = serializers.CharField(max_length=1000, required=False, allow_blank=True)
    logo_url = serializers.URLField(required=False, allow_blank=True)
    
    def validate_name(self, value):
        """Validate club name."""
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Club name must be at least 3 characters long.")
        if len(value.strip()) > 255:
            raise serializers.ValidationError("Club name must not exceed 255 characters.")
        
        # Check if club name already exists
        existing = Club.objects(name__iexact=value.strip())
        if existing:
            raise serializers.ValidationError("A club with this name already exists.")
        
        return value.strip()


class JoinClubSerializer(serializers.Serializer):
    """Serializer for joining a club."""
    club_id = serializers.CharField(required=True)


class LeaveClubSerializer(serializers.Serializer):
    """Serializer for leaving a club."""
    club_id = serializers.CharField(required=True)


class UpdateClubSerializer(serializers.Serializer):
    """Serializer for updating club info."""
    name = serializers.CharField(max_length=255, required=False)
    description = serializers.CharField(max_length=1000, required=False, allow_blank=True)
    logo_url = serializers.URLField(required=False, allow_blank=True)


class ClubStatsSerializer(serializers.Serializer):
    """Serializer for club statistics."""
    club_id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    member_count = serializers.IntegerField(read_only=True)
    total_tournaments = serializers.IntegerField(read_only=True)
    total_wins = serializers.IntegerField(read_only=True)
    win_rate = serializers.SerializerMethodField(read_only=True)
    stats = serializers.DictField(read_only=True)
    
    def get_win_rate(self, obj):
        """Calculate win rate."""
        if obj.total_tournaments == 0:
            return 0
        return round((obj.total_wins / obj.total_tournaments) * 100, 2)


class UserClubsSerializer(serializers.Serializer):
    """Serializer for user's club memberships."""
    club_id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    owner_username = serializers.CharField(read_only=True)
    member_count = serializers.IntegerField(read_only=True)
    total_wins = serializers.IntegerField(read_only=True)
    role = serializers.CharField(read_only=True)
    joined_at = serializers.DateTimeField(read_only=True)
