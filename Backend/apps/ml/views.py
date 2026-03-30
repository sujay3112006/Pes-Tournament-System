"""ML App Views - Prediction API Endpoints"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
import logging

from .serializers import PredictionRequestSerializer, PredictionResponseSerializer, ModelStatsSerializer
from .predictor import get_predictor
from .models import MLModel

logger = logging.getLogger(__name__)


class PredictMatchWinnerView(APIView):
    """Predict win probability for a match between two players.
    
    POST /api/v1/ml/predict/
    {
        "player1_id": "uuid",
        "player2_id": "uuid",
        "use_cache": true
    }
    
    Returns:
    {
        "player1_id": "uuid",
        "player2_id": "uuid",
        "player1_win_probability": 0.65,
        "player2_win_probability": 0.35,
        "confidence": 0.82,
        "predicted_at": "2026-03-30T10:30:00",
        "cached": false
    }
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Predict match outcome."""
        try:
            # Validate request
            serializer = PredictionRequestSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {
                        'success': False,
                        'errors': serializer.errors,
                        'message': 'Invalid prediction request'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            player1_id = serializer.validated_data['player1_id']
            player2_id = serializer.validated_data['player2_id']
            use_cache = serializer.validated_data.get('use_cache', True)
            
            # Get predictor and make prediction
            predictor = get_predictor()
            prediction = predictor.predict(player1_id, player2_id, use_cache=use_cache)
            
            # Validate response
            response_serializer = PredictionResponseSerializer(data=prediction)
            if not response_serializer.is_valid():
                logger.error(f"Invalid prediction response: {response_serializer.errors}")
                prediction['player1_win_probability'] = round(prediction['player1_win_probability'], 4)
                prediction['player2_win_probability'] = round(prediction['player2_win_probability'], 4)
            
            return Response(
                {
                    'success': True,
                    'data': prediction,
                    'message': 'Prediction successful'
                },
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            logger.error(f"Error in prediction: {str(e)}")
            return Response(
                {
                    'success': False,
                    'error': str(e),
                    'message': 'Prediction failed'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ModelStatsView(APIView):
    """Get active ML model statistics.
    
    GET /api/v1/ml/model-stats/
    
    Returns model version, accuracy, metrics, and status.
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Get active model statistics."""
        try:
            active_model = MLModel.objects(is_active=True).first()
            
            if not active_model:
                return Response(
                    {
                        'success': False,
                        'message': 'No active model found',
                        'data': None
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            
            data = {
                'model_name': active_model.model_name,
                'model_type': active_model.model_type,
                'version': active_model.version,
                'accuracy': active_model.accuracy or {},
                'metrics': active_model.metrics or {},
                'training_samples': active_model.training_samples or 0,
                'trained_at': active_model.trained_at.isoformat() if active_model.trained_at else None,
                'is_active': active_model.is_active,
                'status': active_model.status,
            }
            
            response_serializer = ModelStatsSerializer(data=data)
            if not response_serializer.is_valid():
                logger.warning(f"Invalid model stats response: {response_serializer.errors}")
            
            return Response(
                {
                    'success': True,
                    'data': data,
                    'message': 'Model statistics retrieved'
                },
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            logger.error(f"Error retrieving model stats: {str(e)}")
            return Response(
                {
                    'success': False,
                    'error': str(e),
                    'message': 'Failed to retrieve model statistics'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ReloadModelView(APIView):
    """Reload ML model from disk (admin only in production).
    
    POST /api/v1/ml/reload-model/
    
    Useful after training a new model.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Reload model from disk."""
        try:
            # In production, add admin check
            if not request.user.is_staff:
                return Response(
                    {
                        'success': False,
                        'message': 'Permission denied'
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Import here to get fresh instance
            from apps.ml.predictor import WinProbabilityPredictor
            predictor = WinProbabilityPredictor()
            
            if predictor.model is None:
                return Response(
                    {
                        'success': False,
                        'message': 'Failed to load model'
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            return Response(
                {
                    'success': True,
                    'message': 'Model reloaded successfully'
                },
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            logger.error(f"Error reloading model: {str(e)}")
            return Response(
                {
                    'success': False,
                    'error': str(e),
                    'message': 'Failed to reload model'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
