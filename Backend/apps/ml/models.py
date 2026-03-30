"""ML App Models - Store ML model metadata"""
from mongoengine import Document, StringField, DateTimeField, BooleanField, DynamicField, IntField
from datetime import datetime
import uuid


class MLModel(Document):
    """Store metadata about trained ML models."""
    model_id = StringField(unique=True, required=True, default=lambda: str(uuid.uuid4()))
    model_name = StringField(required=True, default='win_probability_model')
    model_type = StringField(required=True, default='random_forest')  # random_forest, logistic_regression, xgboost
    version = IntField(default=1)
    is_active = BooleanField(default=False)
    accuracy = DynamicField()  # {train_accuracy, test_accuracy}
    metrics = DynamicField(default={})  # {precision, recall, f1, auc, etc}
    training_samples = IntField()
    trained_at = DateTimeField(required=True)
    features_used = DynamicField(default=[])  # List of feature names
    model_path = StringField()  # Path to pickled model
    status = StringField(choices=['training', 'completed', 'failed'], default='training')
    error_message = StringField(blank=True)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'ml_models',
        'indexes': ['model_id', 'is_active', 'created_at'],
    }
    
    def __str__(self):
        return f"{self.model_name} v{self.version} ({self.status})"


class PredictionCache(Document):
    """Cache predictions for performance."""
    cache_id = StringField(unique=True, required=True, default=lambda: str(uuid.uuid4()))
    player1_id = StringField(required=True)
    player2_id = StringField(required=True)
    player1_win_probability = DynamicField()  # Float 0-1
    player2_win_probability = DynamicField()  # Float 0-1
    predicted_at = DateTimeField(required=True)
    expires_at = DateTimeField(required=True)  # Cache expiry
    is_valid = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'prediction_cache',
        'indexes': ['player1_id', 'player2_id', 'expires_at'],
    }
    
    def __str__(self):
        return f"Prediction: {self.player1_id} vs {self.player2_id}"
