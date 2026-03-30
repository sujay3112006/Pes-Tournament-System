"""Leaderboard App Models"""
from mongoengine import Document, StringField, DateTimeField, IntField, DynamicField
from datetime import datetime
import uuid


class Leaderboard(Document):
    """Leaderboard for tournaments."""
    leaderboard_id = StringField(unique=True, required=True, default=lambda: str(uuid.uuid4()))
    tournament_id = StringField(required=True, unique=True)
    total_entries = IntField(default=0)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'leaderboards',
        'indexes': ['tournament_id', 'updated_at'],
    }
    
    def __str__(self):
        return f"Leaderboard for {self.tournament_id}"


class LeaderboardEntry(Document):
    """Individual leaderboard entry."""
    entry_id = StringField(unique=True, required=True, default=lambda: str(uuid.uuid4()))
    tournament_id = StringField(required=True, unique_with='user_id')
    user_id = StringField(required=True)  # Reference to User.user_id
    username = StringField(required=True)
    rank = IntField()
    points = IntField(default=0)
    matches_played = IntField(default=0)
    wins = IntField(default=0)
    losses = IntField(default=0)
    draws = IntField(default=0)
    goal_difference = IntField(default=0)
    updated_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'leaderboard_entries',
        'indexes': ['tournament_id', 'user_id', ('tournament_id', 'rank')],
    }
    
    def __str__(self):
        return f"#{self.rank} {self.username} - {self.points} pts"
