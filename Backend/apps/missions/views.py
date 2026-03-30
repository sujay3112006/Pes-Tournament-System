"""Missions App Views"""
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from datetime import datetime

from apps.missions.models import Mission, UserMission
from apps.missions.serializers import (
    MissionSerializer,
    UserMissionSerializer,
    UserMissionDetailSerializer,
    UpdateMissionProgressSerializer,
    ClaimRewardSerializer,
    MissionStatsSerializer,
    CompletedMissionSerializer,
    MissionProgressUpdateResponseSerializer,
)
import uuid
import logging

logger = logging.getLogger(__name__)


class AvailableMissionsView(generics.ListAPIView):
    """Get all available missions."""
    serializer_class = MissionSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        mission_type = self.request.query_params.get('type')
        queryset = Mission.objects(status='active')
        
        if mission_type:
            queryset = queryset(mission_type=mission_type)
        
        # Filter by date range
        now = timezone.now()
        queryset = queryset(start_date__lte=now, end_date__gte=now)
        
        return queryset.order_by('-created_at')
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': len(queryset),
            'missions': serializer.data,
        })


class UserMissionsView(generics.ListAPIView):
    """Get user's missions."""
    serializer_class = UserMissionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user_id = self.request.user.user_id
        status_filter = self.request.query_params.get('status')
        
        if status_filter == 'completed':
            queryset = UserMission.objects(user_id=user_id, completed=True)
        elif status_filter == 'active':
            queryset = UserMission.objects(user_id=user_id, completed=False)
        elif status_filter == 'unclaimed':
            queryset = UserMission.objects(
                user_id=user_id,
                completed=True,
                reward_claimed=False
            )
        else:
            queryset = UserMission.objects(user_id=user_id)
        
        return queryset.order_by('-started_at')
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': len(queryset),
            'missions': serializer.data,
        })


class UserMissionDetailView(generics.GenericAPIView):
    """Get detailed view of user's specific mission."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, mission_id, *args, **kwargs):
        try:
            user_mission = UserMission.objects.get(
                user_id=request.user.user_id,
                mission_id=mission_id
            )
            
            # Try to get mission details
            try:
                mission = Mission.objects.get(mission_id=mission_id)
                data = UserMissionDetailSerializer(user_mission).data
                data['mission_description'] = mission.description
                data['mission_type'] = mission.mission_type
                data['difficulty'] = mission.difficulty
                data['reward'] = mission.reward
                return Response(data)
            except Mission.DoesNotExist:
                serializer = UserMissionDetailSerializer(user_mission)
                return Response(serializer.data)
        except UserMission.DoesNotExist:
            return Response(
                {'error': 'Mission not found for user'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error retrieving mission detail: {str(e)}")
            return Response(
                {'error': 'Failed to retrieve mission'},
                status=status.HTTP_400_BAD_REQUEST
            )


class UpdateMissionProgressView(generics.GenericAPIView):
    """Update user mission progress."""
    serializer_class = UpdateMissionProgressSerializer
    permission_classes = [IsAuthenticated]
    
    def put(self, request, mission_id, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            user_mission = UserMission.objects.get(
                user_id=request.user.user_id,
                mission_id=mission_id
            )
            
            if user_mission.completed and user_mission.reward_claimed:
                return Response(
                    {'error': 'Mission already completed and reward claimed'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Update progress
            progress_increment = serializer.validated_data['progress_increment']
            user_mission.progress += progress_increment
            
            # Check if mission is completed
            if user_mission.progress >= user_mission.condition_value:
                user_mission.progress = user_mission.condition_value
                user_mission.completed = True
                user_mission.completed_at = timezone.now()
            
            user_mission.save()
            
            # Calculate progress percentage
            progress_percentage = round(
                (user_mission.progress / user_mission.condition_value) * 100, 2
            )
            
            return Response(
                {
                    'message': 'Progress updated successfully',
                    'progress': user_mission.progress,
                    'condition_value': user_mission.condition_value,
                    'progress_percentage': progress_percentage,
                    'completed': user_mission.completed,
                    'can_claim_reward': user_mission.completed and not user_mission.reward_claimed,
                },
                status=status.HTTP_200_OK
            )
        except UserMission.DoesNotExist:
            return Response(
                {'error': 'Mission not found for user'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error updating mission progress: {str(e)}")
            return Response(
                {'error': 'Failed to update mission progress'},
                status=status.HTTP_400_BAD_REQUEST
            )


class ClaimRewardView(generics.GenericAPIView):
    """Claim rewards for completed mission."""
    serializer_class = ClaimRewardSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        mission_id = serializer.validated_data['mission_id']
        user_id = request.user.user_id
        
        try:
            user_mission = UserMission.objects.get(
                user_id=user_id,
                mission_id=mission_id
            )
            
            # Check if mission is completed
            if not user_mission.completed:
                return Response(
                    {'error': 'Mission not completed yet'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check if reward already claimed
            if user_mission.reward_claimed:
                return Response(
                    {'error': 'Reward already claimed'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get mission details for rewards
            try:
                mission = Mission.objects.get(mission_id=mission_id)
                reward = mission.reward
            except Mission.DoesNotExist:
                return Response(
                    {'error': 'Mission not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Award coins and points
            try:
                from apps.users.models import User, UserStatistics
                user = User.objects.get(user_id=user_id)
                
                coins_awarded = reward.get('coins', 0)
                points_awarded = reward.get('points', 0)
                
                if coins_awarded > 0:
                    user.coins += coins_awarded
                if points_awarded > 0:
                    # Award to user statistics
                    stats = UserStatistics.objects.get(user_id=user_id)
                    stats.total_points += points_awarded
                    stats.save()
                
                user.save()
            except Exception as e:
                logger.error(f"Error awarding coins/points: {str(e)}")
                return Response(
                    {'error': 'Failed to award rewards'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Mark reward as claimed
            user_mission.reward_claimed = True
            user_mission.claimed_at = timezone.now()
            user_mission.save()
            
            return Response(
                {
                    'message': 'Reward claimed successfully',
                    'coins_awarded': coins_awarded,
                    'points_awarded': points_awarded,
                    'user_coins': user.coins,
                },
                status=status.HTTP_200_OK
            )
        except UserMission.DoesNotExist:
            return Response(
                {'error': 'Mission not found for user'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error claiming reward: {str(e)}")
            return Response(
                {'error': 'Failed to claim reward'},
                status=status.HTTP_400_BAD_REQUEST
            )


class PendingRewardsView(generics.ListAPIView):
    """Get user's completed but unclaimed missions."""
    serializer_class = CompletedMissionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user_id = self.request.user.user_id
        return UserMission.objects(
            user_id=user_id,
            completed=True,
            reward_claimed=False
        ).order_by('-completed_at')
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # Enrich with mission reward data
        enriched_data = []
        for user_mission in queryset:
            try:
                mission = Mission.objects.get(mission_id=user_mission.mission_id)
                data = CompletedMissionSerializer(user_mission).data
                data['reward'] = mission.reward
                data['difficulty'] = mission.difficulty
                enriched_data.append(data)
            except Mission.DoesNotExist:
                enriched_data.append(CompletedMissionSerializer(user_mission).data)
        
        return Response({
            'count': len(enriched_data),
            'pending_rewards': enriched_data,
        })


class UserMissionStatsView(generics.GenericAPIView):
    """Get user's mission statistics."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user_id = request.user.user_id
        
        try:
            total_missions = len(UserMission.objects(user_id=user_id))
            completed_missions = len(UserMission.objects(
                user_id=user_id,
                completed=True
            ))
            active_missions = len(UserMission.objects(
                user_id=user_id,
                completed=False
            ))
            pending_rewards = len(UserMission.objects(
                user_id=user_id,
                completed=True,
                reward_claimed=False
            ))
            
            # Calculate total coins and points from missions
            claimed_missions = UserMission.objects(
                user_id=user_id,
                reward_claimed=True
            )
            
            total_coins = 0
            total_points = 0
            for user_mission in claimed_missions:
                try:
                    mission = Mission.objects.get(mission_id=user_mission.mission_id)
                    total_coins += mission.reward.get('coins', 0)
                    total_points += mission.reward.get('points', 0)
                except:
                    pass
            
            return Response({
                'total_missions': total_missions,
                'completed_missions': completed_missions,
                'active_missions': active_missions,
                'pending_rewards': pending_rewards,
                'total_coins_from_missions': total_coins,
                'total_points_from_missions': total_points,
            })
        except Exception as e:
            logger.error(f"Error getting mission stats: {str(e)}")
            return Response(
                {'error': 'Failed to retrieve statistics'},
                status=status.HTTP_400_BAD_REQUEST
            )


class StartMissionView(generics.GenericAPIView):
    """Start a new mission for user."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, mission_id, *args, **kwargs):
        try:
            # Get mission
            mission = Mission.objects.get(mission_id=mission_id)
            
            # Check if user already has this mission
            existing = UserMission.objects(
                user_id=request.user.user_id,
                mission_id=mission_id
            )
            if existing:
                return Response(
                    {'error': 'User already has this mission'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create user mission
            condition_value = mission.condition.get('value', 1)
            user_mission = UserMission(
                user_mission_id=str(uuid.uuid4()),
                user_id=request.user.user_id,
                mission_id=mission_id,
                mission_title=mission.title,
                progress=0,
                condition_value=condition_value,
            )
            user_mission.save()
            
            return Response(
                {
                    'message': 'Mission started successfully',
                    'user_mission_id': user_mission.user_mission_id,
                    'mission_id': mission_id,
                    'title': mission.title,
                },
                status=status.HTTP_201_CREATED
            )
        except Mission.DoesNotExist:
            return Response(
                {'error': 'Mission not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error starting mission: {str(e)}")
            return Response(
                {'error': 'Failed to start mission'},
                status=status.HTTP_400_BAD_REQUEST
            )
