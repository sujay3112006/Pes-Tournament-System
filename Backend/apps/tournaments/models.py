"""Tournaments App Models"""
from mongoengine import Document, StringField, DateTimeField, IntField, BooleanField, ListField, DynamicField, URLField
from datetime import datetime


class Tournament(Document):
    """Tournament model."""
    tournament_id = StringField(unique=True, required=True)
    name = StringField(required=True, max_length=255)
    description = StringField(max_length=1000)
    creator_id = StringField(required=True)
    banner_image = URLField()
    start_date = DateTimeField(required=True)
    end_date = DateTimeField(required=True)
    total_teams = IntField(default=0)
    status = StringField(choices=['draft', 'active', 'completed', 'cancelled'], default='draft')
    tournament_type = StringField(choices=['league', 'knockout', 'group', 'round_robin'])
    max_teams = IntField(default=16)
    rules = StringField()
    prize_pool = StringField(default=0)
    location = StringField()
    is_public = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'tournaments',
        'indexes': ['tournament_id', 'creator_id', 'status'],
    }
    
    def __str__(self):
        return f"{self.name} - {self.status}"


class TournamentTeam(Document):
    """Teams in a tournament."""
    tournament_id = StringField(required=True)
    team_id = StringField(required=True, unique_with='tournament_id')
    team_name = StringField(required=True)
    captain_id = StringField(required=True)
    members = ListField(StringField())
    joined_at = DateTimeField(default=datetime.now)
    status = StringField(choices=['active', 'eliminated', 'withdrawn'], default='active')
    points = IntField(default=0)
    matches_played = IntField(default=0)
    wins = IntField(default=0)
    draws = IntField(default=0)
    losses = IntField(default=0)
    
    meta = {
        'collection': 'tournament_teams',
        'indexes': ['tournament_id', 'team_id'],
    }
    
    def __str__(self):
        return f"{self.team_name} - {self.tournament_id}"
