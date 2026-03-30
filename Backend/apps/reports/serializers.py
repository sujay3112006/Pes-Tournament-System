"""Reports App Serializers"""
from rest_framework import serializers
from django.utils import timezone
from .models import Report


class ReportListSerializer(serializers.ModelSerializer):
    """Serializer for listing reports."""
    report_id = serializers.CharField(source='report_id', read_only=True)
    reported_by_username = serializers.SerializerMethodField()
    reported_player_username = serializers.SerializerMethodField()
    reviewer_username = serializers.SerializerMethodField()
    
    class Meta:
        model = Report
        fields = ['report_id', 'match_id', 'reported_by_id', 'reported_by_username', 
                  'reported_player_id', 'reported_player_username', 'status', 'severity',
                  'created_at', 'reviewed_by', 'reviewer_username']
        read_only_fields = ['report_id', 'created_at']
    
    def get_reported_by_username(self, obj):
        """Get reporter username."""
        from apps.auth.models import User
        try:
            user = User.objects.get(user_id=obj.reported_by_id)
            return user.username
        except:
            return None
    
    def get_reported_player_username(self, obj):
        """Get reported player username."""
        from apps.auth.models import User
        try:
            user = User.objects.get(user_id=obj.reported_player_id)
            return user.username
        except:
            return None
    
    def get_reviewer_username(self, obj):
        """Get reviewer username."""
        if not obj.reviewed_by:
            return None
        from apps.auth.models import User
        try:
            user = User.objects.get(user_id=obj.reviewed_by)
            return user.username
        except:
            return None


class ReportDetailSerializer(serializers.ModelSerializer):
    """Serializer for report detail view."""
    report_id = serializers.CharField(source='report_id', read_only=True)
    reported_by_username = serializers.SerializerMethodField()
    reported_player_username = serializers.SerializerMethodField()
    reviewer_username = serializers.SerializerMethodField()
    proof_files_count = serializers.SerializerMethodField()
    days_since_report = serializers.SerializerMethodField()
    
    class Meta:
        model = Report
        fields = ['report_id', 'match_id', 'reported_by_id', 'reported_by_username',
                  'reported_player_id', 'reported_player_username', 'reason', 'description',
                  'status', 'severity', 'action_taken', 'proof_files_count', 'proof_urls',
                  'reviewed_by', 'reviewer_username', 'resolved_at', 'resolution_notes',
                  'created_at', 'updated_at', 'days_since_report']
        read_only_fields = ['report_id', 'created_at', 'updated_at']
    
    def get_reported_by_username(self, obj):
        """Get reporter username."""
        from apps.auth.models import User
        try:
            user = User.objects.get(user_id=obj.reported_by_id)
            return user.username
        except:
            return None
    
    def get_reported_player_username(self, obj):
        """Get reported player username."""
        from apps.auth.models import User
        try:
            user = User.objects.get(user_id=obj.reported_player_id)
            return user.username
        except:
            return None
    
    def get_reviewer_username(self, obj):
        """Get reviewer username."""
        if not obj.reviewed_by:
            return None
        from apps.auth.models import User
        try:
            user = User.objects.get(user_id=obj.reviewed_by)
            return user.username
        except:
            return None
    
    def get_proof_files_count(self, obj):
        """Count proof files."""
        try:
            if obj.proof_files:
                return len(obj.proof_files) if isinstance(obj.proof_files, list) else 1
            return 0
        except:
            return 0
    
    def get_days_since_report(self, obj):
        """Calculate days since report creation."""
        delta = timezone.now() - obj.created_at
        return delta.days


class CreateReportSerializer(serializers.ModelSerializer):
    """Serializer for creating reports with file upload."""
    proof_files = serializers.ListField(
        child=serializers.FileField(max_length=100000),
        required=False,
        allow_empty=True
    )
    
    class Meta:
        model = Report
        fields = ['match_id', 'reported_player_id', 'reason', 'description', 
                  'severity', 'proof_files', 'proof_urls']
    
    def validate_reason(self, value):
        """Validate reason field."""
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Reason is required")
        if len(value) > 1000:
            raise serializers.ValidationError("Reason must not exceed 1000 characters")
        return value
    
    def validate_severity(self, value):
        """Validate severity."""
        valid_choices = ['low', 'medium', 'high', 'critical']
        if value not in valid_choices:
            raise serializers.ValidationError(f"Severity must be one of: {', '.join(valid_choices)}")
        return value
    
    def validate_proof_files(self, value):
        """Validate proof files."""
        if value:
            for file in value:
                # Check file size (10MB limit)
                if file.size > 10 * 1024 * 1024:
                    raise serializers.ValidationError(f"File {file.name} exceeds 10MB limit")
                
                # Check file type
                allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf', 
                               'video/mp4', 'video/quicktime']
                if file.content_type not in allowed_types:
                    raise serializers.ValidationError(f"File type {file.content_type} not allowed")
        return value
    
    def create(self, validated_data):
        """Create report with file handling."""
        from apps.auth.models import User
        request = self.context.get('request')
        user_id = request.user.user_id if hasattr(request.user, 'user_id') else request.user.id
        
        proof_files = validated_data.pop('proof_files', [])
        
        report = Report.objects.create(
            reported_by_id=user_id,
            **validated_data
        )
        
        # Store proof files
        if proof_files:
            report.proof_files = proof_files
            report.save()
        
        return report


class ReviewReportSerializer(serializers.Serializer):
    """Serializer for marking report under review."""
    
    def update(self, instance, validated_data):
        """Mark report under review."""
        from apps.auth.models import User
        request = self.context.get('request')
        user_id = request.user.user_id if hasattr(request.user, 'user_id') else request.user.id
        
        instance.status = 'under_review'
        instance.reviewed_by = user_id
        instance.save()
        return instance


class ApproveReportSerializer(serializers.Serializer):
    """Serializer for approving report."""
    action_taken = serializers.ChoiceField(choices=['match_voided', 'player_banned', 'none'])
    resolution_notes = serializers.CharField(required=False, allow_blank=True, max_length=2000)
    
    def validate_action_taken(self, value):
        """Validate action taken."""
        valid_actions = ['match_voided', 'player_banned', 'none']
        if value not in valid_actions:
            raise serializers.ValidationError(f"Action must be one of: {', '.join(valid_actions)}")
        return value
    
    def update(self, instance, validated_data):
        """Approve report with action."""
        from apps.auth.models import User
        request = self.context.get('request')
        user_id = request.user.user_id if hasattr(request.user, 'user_id') else request.user.id
        
        instance.status = 'resolved'
        instance.action_taken = validated_data.get('action_taken', 'none')
        instance.resolution_notes = validated_data.get('resolution_notes', '')
        instance.reviewed_by = user_id
        instance.resolved_at = timezone.now()
        instance.save()
        return instance


class RejectReportSerializer(serializers.Serializer):
    """Serializer for rejecting report."""
    resolution_notes = serializers.CharField(required=False, allow_blank=True, max_length=2000)
    
    def update(self, instance, validated_data):
        """Reject report."""
        from apps.auth.models import User
        request = self.context.get('request')
        user_id = request.user.user_id if hasattr(request.user, 'user_id') else request.user.id
        
        instance.status = 'rejected'
        instance.resolution_notes = validated_data.get('resolution_notes', '')
        instance.reviewed_by = user_id
        instance.resolved_at = timezone.now()
        instance.save()
        return instance


class ReportStatsSerializer(serializers.Serializer):
    """Serializer for report statistics."""
    total_reports = serializers.IntegerField()
    pending_reports = serializers.IntegerField()
    under_review_reports = serializers.IntegerField()
    resolved_reports = serializers.IntegerField()
    rejected_reports = serializers.IntegerField()
    severe_reports = serializers.IntegerField()
    average_resolution_time = serializers.CharField()
    most_common_reason = serializers.CharField()
    most_reported_player = serializers.CharField()
