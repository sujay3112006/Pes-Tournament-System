"""Missions App Models"""
from mongoengine import Document, StringField, DateTimeField, IntField, BooleanField, ListField, DynamicField
from datetime import datetime
import uuid


class Mission(Document):
    """Mission/Quest model."""
    mission_id = StringField(unique=True, required=True, default=lambda: str(uuid.uuid4()))
    title = StringField(required=True, max_length=255)
    description = StringField(max_length=1000, blank=True)
    mission_type = StringField(choices=['daily', 'weekly', 'seasonal', 'special'], required=True)
    reward = DynamicField(required=True)  # {coins: 100, points: 50, badge_id: null}
    condition = DynamicField(required=True)  # {type: 'wins', value: 5} or {type: 'matches_played', value: 10}
    difficulty = StringField(choices=['easy', 'medium', 'hard', 'expert'], default='medium')
    status = StringField(choices=['active', 'inactive', 'archived'], default='active')
    start_date = DateTimeField()
    end_date = DateTimeField()
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'missions',
        'indexes': ['mission_id', 'mission_type', 'status'],
    }
    
    def __str__(self):
        return f"{self.title} ({self.mission_type})"


class UserMission(Document):
    """User mission progress."""
    user_mission_id = StringField(unique=True, required=True, default=lambda: str(uuid.uuid4()))
    user_id = StringField(required=True)  # Reference to User.user_id
    mission_id = StringField(required=True, unique_with='user_id')
    mission_title = StringField(required=True)
    progress = IntField(default=0)
    condition_value = IntField()  # Target value to complete
    completed = BooleanField(default=False)
    completed_at = DateTimeField(blank=True, null=True)
    reward_claimed = BooleanField(default=False)
    claimed_at = DateTimeField(blank=True, null=True)
    started_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'user_missions',
        'indexes': ['user_id', 'mission_id', ('user_id', 'completed')],
    }
    
    def __str__(self):
        status = 'DONE' if self.completed else f"{self.progress}/{self.condition_value}"
        return f"{self.mission_title} - {status}"
