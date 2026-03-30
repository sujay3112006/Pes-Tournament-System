"""Matches App Models"""
from mongoengine import Document, StringField, DateTimeField, IntField, BooleanField, ListField, URLField, DynamicField, FileField
from datetime import datetime
import uuid


class Match(Document):
    """Match model."""
    match_id = StringField(unique=True, required=True, default=lambda: str(uuid.uuid4()))
    tournament_id = StringField(required=True)
    player1_id = StringField(required=True)  # Reference to User.user_id
    player2_id = StringField(required=True)  # Reference to User.user_id
    player1_username = StringField(required=True)
    player2_username = StringField(required=True)
    match_date = DateTimeField(required=True)
    status = StringField(choices=['scheduled', 'live', 'completed', 'cancelled', 'disputed'], default='scheduled')
    score = DynamicField(default={})  # {player1: 0, player2: 0}
    winner_id = StringField(blank=True, null=True)  # User.user_id of winner
    loser_id = StringField(blank=True, null=True)
    proof = FileField(blank=True, null=True)  # Screenshot/proof file
    proof_url = URLField(blank=True, null=True)  # URL if stored separately
    location = StringField(blank=True)
    duration = IntField(blank=True, null=True)  # in minutes
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'matches',
        'indexes': ['match_id', 'tournament_id', 'status', 'match_date'],
    }
    
    def __str__(self):
        return f"{self.player1_username} vs {self.player2_username} - {self.status}"


class MatchEvent(Document):
    """Match events (detailed history)."""
    event_id = StringField(unique=True, required=True, default=lambda: str(uuid.uuid4()))
    match_id = StringField(required=True)
    event_type = StringField(choices=['goal', 'yellow_card', 'red_card', 'substitution', 'own_goal', 'system'], required=True)
    player_id = StringField(required=True)
    team_id = StringField()
    minute = IntField()
    description = StringField(blank=True)
    created_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'match_events',
        'indexes': ['match_id', 'event_type'],
    }
    
    def __str__(self):
        return f"{self.event_type} @ {self.minute}' in {self.match_id}"
