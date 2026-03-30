"""Leaderboard App Models"""
from mongoengine import Document, StringField, DateTimeField, IntField
from datetime import datetime


class Leaderboard(Document):
    """Leaderboard for tournaments."""
    leaderboard_id = StringField(unique=True, required=True)
    tournament_id = StringField(required=True, unique=True)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'leaderboards',
        'indexes': ['tournament_id'],
    }


class LeaderboardEntry(Document):
    """Individual leaderboard entry."""
    leaderboard_id = StringField(required=True)
    rank = IntField()
    team_id = StringField(required=True, unique_with='leaderboard_id')
    team_name = StringField()
    points = IntField(default=0)
    matches_played = IntField(default=0)
    wins = IntField(default=0)
    draws = IntField(default=0)
    losses = IntField(default=0)
    goal_for = IntField(default=0)
    goal_against = IntField(default=0)
    goal_difference = IntField(default=0)
    updated_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'leaderboard_entries',
        'indexes': ['leaderboard_id', 'team_id'],
    }
    
    def __str__(self):
        return f"{self.rank}. {self.team_name} - {self.points}pts"
