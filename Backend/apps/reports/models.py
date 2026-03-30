"""Reports App Models"""
from mongoengine import Document, StringField, DateTimeField, IntField, BooleanField
from datetime import datetime


class Report(Document):
    """User/Match report model."""
    report_id = StringField(unique=True, required=True)
    report_type = StringField(choices=['user', 'match', 'comment', 'other'], required=True)
    reported_by_id = StringField(required=True)
    reported_item_id = StringField(required=True)
    reason = StringField(required=True, max_length=500)
    description = StringField(max_length=1000)
    status = StringField(choices=['pending', 'under_review', 'resolved', 'rejected'], default='pending')
    severity = StringField(choices=['low', 'medium', 'high', 'critical'], default='medium')
    action_taken = StringField()
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    resolved_by = StringField()
    resolved_at = DateTimeField()
    
    meta = {
        'collection': 'reports',
        'indexes': ['report_id', 'report_type', 'status'],
    }
    
    def __str__(self):
        return f"Report - {self.report_type} - {self.status}"
