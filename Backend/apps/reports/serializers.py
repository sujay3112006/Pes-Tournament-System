"""Reports App Serializers"""
from rest_framework import serializers


class ReportSerializer(serializers.Serializer):
    """Report serializer."""
    report_id = serializers.CharField(read_only=True)
    report_type = serializers.ChoiceField(choices=['user', 'match', 'comment', 'other'])
    reported_by_id = serializers.CharField()
    reported_item_id = serializers.CharField()
    reason = serializers.CharField(max_length=500)
    description = serializers.CharField(required=False)
    status = serializers.ChoiceField(choices=['pending', 'under_review', 'resolved', 'rejected'])
    severity = serializers.ChoiceField(choices=['low', 'medium', 'high', 'critical'])
    created_at = serializers.DateTimeField(read_only=True)
