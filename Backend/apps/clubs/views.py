"""Clubs App Views"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.clubs.models import Club, ClubMember
from apps.clubs.serializers import ClubSerializer, ClubMemberSerializer


class ClubViewSet(viewsets.ModelViewSet):
    """Club ViewSet."""
    serializer_class = ClubSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Club.objects()
    
    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        """Join a club."""
        club_id = pk
        
        try:
            club = Club.objects.get(club_id=club_id)
            
            # Check if already a member
            existing_member = ClubMember.objects(club_id=club_id, user_id=str(request.user.id))
            if existing_member:
                return Response(
                    {'error': 'Already a member of this club'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            ClubMember.objects.create(
                member_id=f"{club_id}_{request.user.id}",
                club_id=club_id,
                user_id=str(request.user.id),
                username=request.user.username,
                role='member'
            )
            
            club.members.append(str(request.user.id))
            club.member_count = len(club.members)
            club.save()
            
            return Response({'message': 'Joined club successfully'})
        except Club.DoesNotExist:
            return Response({'error': 'Club not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """Get club members."""
        club_id = pk
        members = ClubMember.objects(club_id=club_id)
        serializer = ClubMemberSerializer(members, many=True)
        return Response(serializer.data)


class ClubMemberViewSet(viewsets.ModelViewSet):
    """Club Member ViewSet."""
    serializer_class = ClubMemberSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ClubMember.objects()
