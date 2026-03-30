"""Clubs App Models"""
from mongoengine import Document, StringField, DateTimeField, IntField, BooleanField, ListField, URLField
from datetime import datetime


class Club(Document):
    """Football Club model."""
    club_id = StringField(unique=True, required=True)
    name = StringField(required=True, max_length=255)
    description = StringField(max_length=1000)
    logo_url = URLField()
    owner_id = StringField(required=True)
    members = ListField(StringField())
    member_count = IntField(default=1)
    founded_date = DateTimeField()
    is_verified = BooleanField(default=False)
    total_tournaments = IntField(default=0)
    total_wins = IntField(default=0)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'clubs',
        'indexes': ['club_id', 'name', 'owner_id'],
    }
    
    def __str__(self):
        return self.name


class ClubMember(Document):
    """Club member record."""
    member_id = StringField(unique=True, required=True)
    club_id = StringField(required=True, unique_with='user_id')
    user_id = StringField(required=True)
    username = StringField()
    role = StringField(choices=['owner', 'admin', 'member'], default='member')
    joined_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'club_members',
        'indexes': ['club_id', 'user_id'],
    }
    
    def __str__(self):
        return f"{self.username} - {self.role}"
