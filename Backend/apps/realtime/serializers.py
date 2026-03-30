"""Realtime App Serializers"""
from rest_framework import serializers


class NotificationSerializer(serializers.Serializer):
    """Notification serializer."""
    notification_id = serializers.CharField(read_only=True)
    user_id = serializers.CharField()
    title = serializers.CharField()
    message = serializers.CharField()
    notification_type = serializers.ChoiceField(choices=['match', 'tournament', 'mission', 'badge', 'system'])
    related_id = serializers.CharField(required=False)
    is_read = serializers.BooleanField()
    created_at = serializers.DateTimeField(read_only=True)
