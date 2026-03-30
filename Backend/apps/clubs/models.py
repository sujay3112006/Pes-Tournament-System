"""Clubs App Models"""
from mongoengine import Document, StringField, DateTimeField, IntField, BooleanField, ListField, URLField, DynamicField
from datetime import datetime
import uuid


class Club(Document):
    """Football Club model."""
    club_id = StringField(unique=True, required=True, default=lambda: str(uuid.uuid4()))
    name = StringField(required=True, max_length=255, unique=True)
    description = StringField(max_length=1000, blank=True)
    logo_url = URLField(blank=True)
    owner_id = StringField(required=True)  # Reference to User.user_id
    owner_username = StringField(required=True)
    members = ListField(StringField())  # List of user_ids
    member_count = IntField(default=1)
    founded_date = DateTimeField()
    is_verified = BooleanField(default=False)
    total_tournaments = IntField(default=0)
    total_wins = IntField(default=0)
    stats = DynamicField(default={})  # {wins, losses, points}
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'clubs',
        'indexes': ['club_id', 'name', 'owner_id'],
    }
    
    def __str__(self):
        return f"{self.name} ({self.member_count} members)"


class ClubMember(Document):
    """Club member record."""
    member_id = StringField(unique=True, required=True, default=lambda: str(uuid.uuid4()))
    club_id = StringField(required=True, unique_with='user_id')
    user_id = StringField(required=True)  # Reference to User.user_id
    username = StringField(required=True)
    role = StringField(choices=['owner', 'admin', 'member'], default='member')
    contribution_score = IntField(default=0)  # Points based on club performance
    joined_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'club_members',
        'indexes': ['club_id', 'user_id', 'role'],
    }
    
    def __str__(self):
        return f"{self.username} ({self.role}) in club"
