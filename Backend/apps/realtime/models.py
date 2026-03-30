"""Realtime App Models"""
from mongoengine import Document, StringField, DateTimeField, DynamicField
from datetime import datetime


class Notification(Document):
    """Notification model."""
    notification_id = StringField(unique=True, required=True)
    user_id = StringField(required=True)
    title = StringField(required=True)
    message = StringField()
    notification_type = StringField(choices=['match', 'tournament', 'mission', 'badge', 'system'])
    related_id = StringField()
    is_read = StringField(default=False)
    data = DynamicField()
    created_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'notifications',
        'indexes': ['user_id', 'is_read'],
    }
    
    def __str__(self):
        return self.title
