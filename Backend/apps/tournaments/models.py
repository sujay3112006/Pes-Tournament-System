"""Tournaments App Models"""
from mongoengine import Document, StringField, DateTimeField, IntField, BooleanField, ListField, DynamicField, URLField, ObjectIdField
from datetime import datetime
import uuid


class Tournament(Document):
    """Tournament model."""
    tournament_id = StringField(unique=True, required=True, default=lambda: str(uuid.uuid4()))
    name = StringField(required=True, max_length=255)
    description = StringField(max_length=1000, blank=True)
    creator_id = StringField(required=True)  # Reference to User.user_id
    banner_image = URLField(blank=True)
    start_date = DateTimeField(required=True)
    end_date = DateTimeField(required=True)
    format = StringField(choices=['Knockout', 'League'], required=True)  # Tournament format
    max_players = IntField(required=True, default=16)
    current_players = IntField(default=0)
    status = StringField(choices=['draft', 'registration', 'active', 'completed', 'cancelled'], default='draft')
    rules = StringField(blank=True)
    prize_pool = DynamicField(default=0)  # Can be coins or money
    location = StringField(blank=True)
    is_public = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'tournaments',
        'indexes': ['tournament_id', 'creator_id', 'status', 'start_date'],
    }
    
    def __str__(self):
        return f"{self.name} ({self.format}) - {self.status}"


class TournamentPlayer(Document):
    """Players in a tournament (junction table)."""
    tournament_player_id = StringField(unique=True, required=True, default=lambda: str(uuid.uuid4()))
    tournament_id = StringField(required=True)
    user_id = StringField(required=True)  # Reference to User.user_id
    username = StringField(required=True)
    joined_at = DateTimeField(default=datetime.now)
    status = StringField(choices=['active', 'eliminated', 'withdrawn', 'disqualified'], default='active')
    points = IntField(default=0)
    matches_played = IntField(default=0)
    wins = IntField(default=0)
    losses = IntField(default=0)
    draws = IntField(default=0)
    
    meta = {
        'collection': 'tournament_players',
        'indexes': ['tournament_id', 'user_id', ('tournament_id', 'user_id')],
    }
    
    def __str__(self):
        return f"{self.username} in {self.tournament_id}"
