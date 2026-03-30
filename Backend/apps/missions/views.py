"""Missions App Views"""
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.missions.models import Mission, UserMission
from apps.missions.serializers import MissionSerializer, UserMissionSerializer


class MissionViewSet(viewsets.ReadOnlyModelViewSet):
    """Mission ViewSet."""
    serializer_class = MissionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Mission.objects()


class UserMissionViewSet(viewsets.ModelViewSet):
    """User Mission ViewSet."""
    serializer_class = UserMissionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserMission.objects(user_id=str(self.request.user.id))
    
    @action(detail=True, methods=['post'])
    def claim_reward(self, request, pk=None):
        """Claim mission reward."""
        try:
            user_mission = UserMission.objects.get(user_mission_id=pk)
            
            if not user_mission.completed:
                return Response(
                    {'error': 'Mission not completed'},
                    status=400
                )
            
            user_mission.claimed = True
            user_mission.save()
            
            return Response({'message': 'Reward claimed successfully'})
        except UserMission.DoesNotExist:
            return Response({'error': 'Mission not found'}, status=404)
