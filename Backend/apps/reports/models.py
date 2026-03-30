"""Reports App - Anti-cheat Reporting"""
from mongoengine import Document, StringField, DateTimeField, IntField, BooleanField, FileField, URLField, ListField, DynamicField
from datetime import datetime
import uuid


class Report(Document):
    """Anti-cheat report model (Match disputes)."""
    report_id = StringField(unique=True, required=True, default=lambda: str(uuid.uuid4()))
    match_id = StringField(required=True)
    reported_by_id = StringField(required=True)  # Reference to User.user_id
    reported_by_username = StringField(required=True)
    reported_player_id = StringField()  # User.user_id of suspected cheater
    reason = StringField(required=True, max_length=500)
    description = StringField(max_length=2000, blank=True)
    proof_files = ListField(FileField())  # Screenshots/evidence
    proof_urls = ListField(URLField())  # URLs if stored separately
    proof_data = DynamicField()  # Additional metadata about proof
    status = StringField(choices=['pending', 'under_review', 'resolved', 'rejected', 'false_claim'], default='pending')
    severity = StringField(choices=['low', 'medium', 'high', 'critical'], default='medium')
    action_taken = StringField(blank=True)  # e.g., 'match_voided', 'player_banned', 'none'
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    reviewed_by = StringField(blank=True, null=True)  # Admin user_id
    resolved_at = DateTimeField(blank=True, null=True)
    resolution_notes = StringField(blank=True)
    
    meta = {
        'collection': 'reports',
        'indexes': ['report_id', 'match_id', 'reported_by_id', 'status', 'created_at'],
    }
    
    def __str__(self):
        return f"Report {self.status.upper()}: {self.reason[:50]}"
