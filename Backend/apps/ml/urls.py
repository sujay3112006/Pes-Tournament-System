"""ML App URLs"""
from django.urls import path
from apps.ml.views import (
    PredictMatchWinnerView,
    ModelStatsView,
    ReloadModelView
)

app_name = 'ml'

urlpatterns = [
    # Prediction endpoints
    path(
        'predict/',
        PredictMatchWinnerView.as_view(),
        name='predict_winner'
    ),
    
    # Model statistics
    path(
        'model-stats/',
        ModelStatsView.as_view(),
        name='model_stats'
    ),
    
    # Reload model
    path(
        'reload-model/',
        ReloadModelView.as_view(),
        name='reload_model'
    ),
]
