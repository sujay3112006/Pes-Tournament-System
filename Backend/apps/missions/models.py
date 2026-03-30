"""Missions App Models"""
from mongoengine import Document, StringField, DateTimeField, IntField, BooleanField, ListField
from datetime import datetime


class Mission(Document):
    """Mission/Quest model."""
    mission_id = StringField(unique=True, required=True)
    title = StringField(required=True, max_length=255)
    description = StringField(max_length=1000)
    mission_type = StringField(choices=['daily', 'weekly', 'seasonal', 'special'])
    reward_points = IntField(required=True)
    reward_badge_id = StringField()
    difficulty = StringField(choices=['easy', 'medium', 'hard', 'expert'], default='medium')
    status = StringField(choices=['active', 'inactive', 'completed'], default='active')
    start_date = DateTimeField()
    end_date = DateTimeField()
    created_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'missions',
        'indexes': ['mission_id', 'mission_type', 'status'],
    }
    
    def __str__(self):
        return self.title


class UserMission(Document):
    """User mission progress."""
    user_mission_id = StringField(unique=True, required=True)
    user_id = StringField(required=True, unique_with='mission_id')
    mission_id = StringField(required=True)
    mission_title = StringField()
    progress = IntField(default=0)
    completed = BooleanField(default=False)
    completed_at = DateTimeField()
    claimed = BooleanField(default=False)
    started_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'user_missions',
        'indexes': ['user_id', 'mission_id'],
    }
    
    def __str__(self):
        return f"{self.user_id} - {self.mission_title}"
