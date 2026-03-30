"""ML Predictor - Load model and make predictions"""
import os
import pickle
import logging
from datetime import datetime, timedelta
import numpy as np
from apps.users.models import UserStatistics
from apps.matches.models import Match
from .models import MLModel, PredictionCache

logger = logging.getLogger(__name__)


class WinProbabilityPredictor:
    """Predictor for match win probability using trained ML model."""
    
    def __init__(self):
        """Initialize predictor."""
        self.model = None
        self.scaler = None
        self.model_path = None
        self.features = None
        self._load_model()
    
    def _load_model(self):
        """Load the active trained model from disk."""
        try:
            # Get active model from database
            active_model = MLModel.objects(is_active=True).first()
            
            if not active_model:
                logger.warning("No active ML model found in database")
                return False
            
            # Load model from disk
            if not os.path.exists(active_model.model_path):
                logger.error(f"Model file not found: {active_model.model_path}")
                return False
            
            with open(active_model.model_path, 'rb') as f:
                model_data = pickle.load(f)
                self.model = model_data.get('model')
                self.scaler = model_data.get('scaler')
                self.features = model_data.get('features')
            
            self.model_path = active_model.model_path
            logger.info(f"Loaded ML model: {active_model.model_name} v{active_model.version}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading ML model: {str(e)}")
            return False
    
    def get_player_features(self, player_id):
        """Extract features for a player from their statistics.
        
        Features extracted:
        - total_matches
        - match_wins
        - match_losses
        - match_draws
        - win_rate
        - goals_scored
        - goals_conceded
        - goal_difference
        - clean_sheets
        - points
        - ranking
        """
        try:
            stats = UserStatistics.objects(user_id=player_id).first()
            
            if not stats:
                logger.warning(f"No statistics found for player {player_id}")
                # Return default features
                return [0.0] * 11
            
            # Calculate derived features
            total_matches = stats.total_matches if stats.total_matches > 0 else 1
            win_rate = stats.match_wins / total_matches if total_matches > 0 else 0.0
            goal_difference = (stats.goals_scored - stats.goals_conceded) if stats.goals_scored and stats.goals_conceded else 0
            
            # Feature vector (11 features)
            features = [
                stats.total_matches,
                stats.match_wins,
                stats.match_losses,
                stats.match_draws,
                win_rate,
                stats.goals_scored or 0,
                stats.goals_conceded or 0,
                goal_difference,
                stats.clean_sheets or 0,
                stats.points or 0,
                stats.ranking if stats.ranking else 999,  # High rank if not ranked
            ]
            
            return features
            
        except Exception as e:
            logger.error(f"Error extracting features for player {player_id}: {str(e)}")
            return [0.0] * 11
    
    def predict(self, player1_id, player2_id, use_cache=True):
        """Predict win probability for two players.
        
        Returns:
            dict with player1_win_prob, player2_win_prob, confidence
        """
        try:
            # Check cache first
            if use_cache:
                cached = self._get_cached_prediction(player1_id, player2_id)
                if cached:
                    return cached
            
            # Load model if not loaded
            if self.model is None:
                if not self._load_model():
                    return self._default_prediction(player1_id, player2_id)
            
            # Get features for both players
            player1_features = self.get_player_features(player1_id)
            player2_features = self.get_player_features(player2_id)
            
            # Create feature difference vector (relative strength)
            # This captures the difference between players
            feature_diff = [
                player1_features[i] - player2_features[i] 
                for i in range(len(player1_features))
            ]
            
            # Scale features
            try:
                feature_diff_scaled = self.scaler.transform([feature_diff])[0]
            except:
                feature_diff_scaled = feature_diff
            
            # Get base statistics for confidence calculation
            stats1 = UserStatistics.objects(user_id=player1_id).first()
            stats2 = UserStatistics.objects(user_id=player2_id).first()
            
            # Predict probability that player1 wins
            try:
                # Use probability prediction if available
                proba = self.model.predict_proba([feature_diff_scaled])
                player1_win_prob = float(proba[0][1])  # Probability of class 1 (player1 wins)
            except:
                # Fallback to prediction
                prediction = self.model.predict([feature_diff_scaled])[0]
                player1_win_prob = 1.0 if prediction == 1 else 0.0
            
            # Confidence is based on player statistics
            player1_matches = stats1.total_matches if stats1 else 0
            player2_matches = stats2.total_matches if stats2 else 0
            avg_matches = (player1_matches + player2_matches) / 2
            confidence = min(avg_matches / 50, 1.0)  # Normalize to [0, 1]
            
            player2_win_prob = 1.0 - player1_win_prob
            
            result = {
                'player1_id': str(player1_id),
                'player2_id': str(player2_id),
                'player1_win_probability': round(player1_win_prob, 4),
                'player2_win_probability': round(player2_win_prob, 4),
                'confidence': round(confidence, 4),
                'predicted_at': datetime.now().isoformat(),
            }
            
            # Cache the result
            if use_cache:
                self._cache_prediction(player1_id, player2_id, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Error predicting match outcome: {str(e)}")
            return self._default_prediction(player1_id, player2_id)
    
    def _default_prediction(self, player1_id, player2_id):
        """Return default 50-50 prediction when model unavailable."""
        return {
            'player1_id': str(player1_id),
            'player2_id': str(player2_id),
            'player1_win_probability': 0.5,
            'player2_win_probability': 0.5,
            'confidence': 0.0,
            'predicted_at': datetime.now().isoformat(),
            'note': 'Model not available, returning default prediction'
        }
    
    def _get_cached_prediction(self, player1_id, player2_id):
        """Get cached prediction if available and not expired."""
        try:
            now = datetime.now()
            cache = PredictionCache.objects(
                player1_id=player1_id,
                player2_id=player2_id,
                is_valid=True,
                expires_at__gt=now
            ).first()
            
            if cache:
                return {
                    'player1_id': str(cache.player1_id),
                    'player2_id': str(cache.player2_id),
                    'player1_win_probability': float(cache.player1_win_probability),
                    'player2_win_probability': float(cache.player2_win_probability),
                    'confidence': 0.0,
                    'predicted_at': cache.predicted_at.isoformat(),
                    'cached': True
                }
        except Exception as e:
            logger.debug(f"Error getting cached prediction: {str(e)}")
        
        return None
    
    def _cache_prediction(self, player1_id, player2_id, result):
        """Cache prediction result."""
        try:
            # Invalidate old cache
            PredictionCache.objects(
                player1_id=player1_id,
                player2_id=player2_id
            ).update(is_valid=False)
            
            # Create new cache entry (1 hour expiry)
            cache = PredictionCache(
                player1_id=player1_id,
                player2_id=player2_id,
                player1_win_probability=result['player1_win_probability'],
                player2_win_probability=result['player2_win_probability'],
                predicted_at=datetime.now(),
                expires_at=datetime.now() + timedelta(hours=1)
            )
            cache.save()
        except Exception as e:
            logger.debug(f"Error caching prediction: {str(e)}")


# Global predictor instance
_predictor = None


def get_predictor():
    """Get or create global predictor instance."""
    global _predictor
    if _predictor is None:
        _predictor = WinProbabilityPredictor()
    return _predictor
