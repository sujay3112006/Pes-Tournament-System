"""ML App Serializers"""
from rest_framework import serializers


class PredictionRequestSerializer(serializers.Serializer):
    """Serializer for prediction request."""
    player1_id = serializers.CharField(required=True)
    player2_id = serializers.CharField(required=True)
    use_cache = serializers.BooleanField(required=False, default=True)
    
    def validate(self, data):
        """Validate that players are not the same."""
        if data.get('player1_id') == data.get('player2_id'):
            raise serializers.ValidationError("Players must be different")
        return data


class PredictionResponseSerializer(serializers.Serializer):
    """Serializer for prediction response."""
    player1_id = serializers.CharField()
    player2_id = serializers.CharField()
    player1_win_probability = serializers.FloatField()
    player2_win_probability = serializers.FloatField()
    confidence = serializers.FloatField()
    predicted_at = serializers.CharField()
    cached = serializers.BooleanField(required=False)
    note = serializers.CharField(required=False)


class ModelStatsSerializer(serializers.Serializer):
    """Serializer for model statistics."""
    model_name = serializers.CharField()
    model_type = serializers.CharField()
    version = serializers.IntegerField()
    accuracy = serializers.DictField()
    metrics = serializers.DictField()
    training_samples = serializers.IntegerField()
    trained_at = serializers.CharField()
    is_active = serializers.BooleanField()
    status = serializers.CharField()
