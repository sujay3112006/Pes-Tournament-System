"""Matches App Models"""
from mongoengine import Document, StringField, DateTimeField, IntField, BooleanField, ListField, URLField
from datetime import datetime


class Match(Document):
    """Match model."""
    match_id = StringField(unique=True, required=True)
    tournament_id = StringField(required=True)
    team_a_id = StringField(required=True)
    team_b_id = StringField(required=True)
    team_a_name = StringField()
    team_b_name = StringField()
    match_date = DateTimeField(required=True)
    status = StringField(choices=['scheduled', 'live', 'completed', 'cancelled'], default='scheduled')
    team_a_score = IntField(default=0)
    team_b_score = IntField(default=0)
    winner_id = StringField()
    location = StringField()
    referee_id = StringField()
    duration = IntField()  # in minutes
    is_played = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'matches',
        'indexes': ['match_id', 'tournament_id', 'status'],
    }
    
    def __str__(self):
        return f"{self.team_a_name} vs {self.team_b_name}"


class MatchEvent(Document):
    """Match events (goals, cards, substitutions)."""
    match_id = StringField(required=True)
    event_type = StringField(choices=['goal', 'yellow_card', 'red_card', 'substitution', 'own_goal'])
    player_id = StringField(required=True)
    team_id = StringField(required=True)
    minute = IntField(required=True)
    description = StringField()
    created_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'match_events',
        'indexes': ['match_id'],
    }
    
    def __str__(self):
        return f"{self.event_type} - {self.minute}'"
