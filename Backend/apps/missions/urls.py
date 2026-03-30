"""Missions App URLs"""
from django.urls import path
from apps.missions.views import (
    AvailableMissionsView,
    UserMissionsView,
    UserMissionDetailView,
    UpdateMissionProgressView,
    ClaimRewardView,
    PendingRewardsView,
    UserMissionStatsView,
    StartMissionView,
)

urlpatterns = [
    # Mission discovery
    path('missions/available/', AvailableMissionsView.as_view(), name='available_missions'),
    path('missions/start/<str:mission_id>/', StartMissionView.as_view(), name='start_mission'),
    
    # User missions
    path('my-missions/', UserMissionsView.as_view(), name='user_missions'),
    path('my-missions/<str:mission_id>/', UserMissionDetailView.as_view(), name='mission_detail'),
    path('my-missions/<str:mission_id>/progress/', UpdateMissionProgressView.as_view(), name='update_progress'),
    
    # Rewards
    path('my-missions/rewards/pending/', PendingRewardsView.as_view(), name='pending_rewards'),
    path('my-missions/rewards/claim/', ClaimRewardView.as_view(), name='claim_reward'),
    
    # Stats
    path('my-missions/stats/', UserMissionStatsView.as_view(), name='mission_stats'),
]
