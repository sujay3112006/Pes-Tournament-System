"""Users App Models"""
from django.contrib.auth.models import AbstractUser
from mongoengine import Document, StringField, EmailField, DateTimeField, BooleanField, URLField, DynamicField, IntField, ReferenceField
import uuid
from datetime import datetime


class User(Document):
    """User model with MongoDB storage."""
    user_id = StringField(unique=True, required=True, default=lambda: str(uuid.uuid4()))
    username = StringField(unique=True, required=True, max_length=150)
    email = EmailField(unique=True, required=True)
    password_hash = StringField(required=True)  # Store hashed password
    first_name = StringField(max_length=150, blank=True)
    last_name = StringField(max_length=150, blank=True)
    coins = IntField(default=0)
    bio = StringField(max_length=500, blank=True)
    avatar_url = URLField(blank=True)
    phone_number = StringField(max_length=20, blank=True)
    birth_date = DateTimeField(blank=True, null=True)
    country = StringField(max_length=100, blank=True)
    stats = DynamicField(default={})  # JSON stats: {wins, losses, tournaments, rating, etc}
    is_verified = BooleanField(default=False)
    is_premium = BooleanField(default=False)
    is_active = BooleanField(default=True)
    last_login = DateTimeField(blank=True, null=True)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'users',
        'indexes': ['user_id', 'username', 'email', 'created_at'],
    }
    
    def __str__(self):
        return f"{self.username} ({self.email})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()


class UserStatistics(Document):
    """User detailed statistics."""
    user_id = StringField(unique=True, required=True)
    total_tournaments = IntField(default=0)
    total_matches = IntField(default=0)
    match_wins = IntField(default=0)
    match_losses = IntField(default=0)
    match_draws = IntField(default=0)
    win_rate = DynamicField(default=0.0)
    goals_scored = IntField(default=0)
    goals_conceded = IntField(default=0)
    clean_sheets = IntField(default=0)
    points = IntField(default=0)
    ranking = IntField()
    updated_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'user_statistics',
        'indexes': ['user_id', 'ranking'],
    }
    
    def __str__(self):
        return f"Stats ({self.user_id}): {self.match_wins}W-{self.match_losses}L"


class UserBadge(Document):
    """User achievement badges."""
    user_id = StringField(required=True)
    badge_name = StringField(required=True, max_length=255)
    badge_icon = URLField()
    description = StringField(max_length=500)
    earned_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'user_badges',
        'indexes': ['user_id', 'earned_at'],
    }
    
    def __str__(self):
        return f"{self.badge_name} - {self.user_id}"
