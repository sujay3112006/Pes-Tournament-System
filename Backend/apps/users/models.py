"""Users App Models"""
from django.contrib.auth.models import AbstractUser
from mongoengine import Document, StringField, EmailField, DateTimeField, BooleanField, URLField
import uuid
from datetime import datetime


class User(AbstractUser):
    """Extended User model with additional fields."""
    user_id = StringField(default=uuid.uuid4, unique=True)
    bio = StringField(max_length=500, blank=True)
    avatar = URLField(blank=True)
    phone_number = StringField(max_length=20, blank=True)
    birth_date = DateTimeField(null=True, blank=True)
    is_verified = BooleanField(default=False)
    is_premium = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.username} ({self.get_full_name()})"


# MongoDB Models using mongoengine
class UserProfile(Document):
    """User profile stored in MongoDB."""
    user_id = StringField(unique=True, required=True)
    username = StringField(unique=True, required=True)
    email = EmailField(unique=True, required=True)
    full_name = StringField(max_length=255)
    bio = StringField(max_length=500)
    avatar_url = URLField()
    phone_number = StringField(max_length=20)
    country = StringField(max_length=100)
    birth_date = DateTimeField()
    is_verified = BooleanField(default=False)
    is_premium = BooleanField(default=False)
    rating = StringField(default='bronze')  # bronze, silver, gold, platinum
    total_tournaments = StringField(default=0)
    total_matches_played = StringField(default=0)
    win_rate = StringField(default=0.0)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    last_login = DateTimeField()
    
    meta = {
        'collection': 'user_profiles',
        'indexes': ['user_id', 'username', 'email'],
    }
    
    def __str__(self):
        return f"{self.username} - {self.email}"


class UserStatistics(Document):
    """User statistics stored in MongoDB."""
    user_id = StringField(unique=True, required=True)
    total_points = StringField(default=0)
    total_badges = StringField(default=0)
    tournament_wins = StringField(default=0)
    match_wins = StringField(default=0)
    match_losses = StringField(default=0)
    match_draws = StringField(default=0)
    goal_scored = StringField(default=0)
    goal_conceded = StringField(default=0)
    clean_sheets = StringField(default=0)
    
    meta = {
        'collection': 'user_statistics',
    }
    
    def __str__(self):
        return f"Stats - {self.user_id}"


class UserBadge(Document):
    """User achievement badges."""
    user_id = StringField(required=True)
    badge_name = StringField(required=True)
    badge_icon = URLField()
    earned_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'user_badges',
        'indexes': ['user_id'],
    }
    
    def __str__(self):
        return f"{self.badge_name} - {self.user_id}"
