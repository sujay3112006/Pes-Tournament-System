"""Clubs App Views"""
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone

from apps.clubs.models import Club, ClubMember
from apps.clubs.serializers import (
    ClubListSerializer,
    ClubDetailSerializer,
    ClubMemberSerializer,
    CreateClubSerializer,
    JoinClubSerializer,
    LeaveClubSerializer,
    UpdateClubSerializer,
    ClubStatsSerializer,
    UserClubsSerializer,
)
import uuid
import logging

logger = logging.getLogger(__name__)


class CreateClubView(generics.GenericAPIView):
    """Create a new club."""
    serializer_class = CreateClubSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            user_id = request.user.user_id
            
            # Create club
            club = Club(
                club_id=str(uuid.uuid4()),
                name=serializer.validated_data['name'],
                description=serializer.validated_data.get('description', ''),
                logo_url=serializer.validated_data.get('logo_url', ''),
                owner_id=user_id,
                owner_username=request.user.username,
                members=[user_id],
                member_count=1,
                founded_date=timezone.now(),
            )
            club.save()
            
            # Add owner as club member
            member = ClubMember(
                member_id=str(uuid.uuid4()),
                club_id=club.club_id,
                user_id=user_id,
                username=request.user.username,
                role='owner',
            )
            member.save()
            
            return Response(
                {
                    'message': 'Club created successfully',
                    'club_id': club.club_id,
                    'name': club.name,
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            logger.error(f"Error creating club: {str(e)}")
            return Response(
                {'error': 'Failed to create club'},
                status=status.HTTP_400_BAD_REQUEST
            )


class AllClubsView(generics.ListAPIView):
    """Get all clubs."""
    serializer_class = ClubListSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = Club.objects().order_by('-created_at')
        
        # Filter by name if provided
        search_query = self.request.query_params.get('search')
        if search_query:
            queryset = queryset(name__icontains=search_query)
        
        # Filter by verified status
        verified = self.request.query_params.get('verified')
        if verified and verified.lower() == 'true':
            queryset = queryset(is_verified=True)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': len(queryset),
            'clubs': serializer.data,
        })


class ClubDetailView(generics.RetrieveAPIView):
    """Get club details."""
    serializer_class = ClubDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'club_id'
    lookup_url_kwarg = 'club_id'
    
    def retrieve(self, request, *args, **kwargs):
        club_id = kwargs.get('club_id')
        
        try:
            club = Club.objects.get(club_id=club_id)
            serializer = self.get_serializer(club)
            return Response(serializer.data)
        except Club.DoesNotExist:
            return Response(
                {'error': 'Club not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error retrieving club: {str(e)}")
            return Response(
                {'error': 'Failed to retrieve club'},
                status=status.HTTP_400_BAD_REQUEST
            )


class JoinClubView(generics.GenericAPIView):
    """Join a club."""
    serializer_class = JoinClubSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        club_id = serializer.validated_data['club_id']
        user_id = request.user.user_id
        
        try:
            # Get club
            club = Club.objects.get(club_id=club_id)
            
            # Check if user is already a member (prevent duplicate)
            existing_member = ClubMember.objects(
                club_id=club_id,
                user_id=user_id
            )
            if existing_member:
                return Response(
                    {'error': 'User is already a member of this club'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Add user to club
            if user_id not in club.members:
                club.members.append(user_id)
                club.member_count += 1
                club.updated_at = timezone.now()
                club.save()
            
            # Create club member record
            member = ClubMember(
                member_id=str(uuid.uuid4()),
                club_id=club_id,
                user_id=user_id,
                username=request.user.username,
                role='member',
            )
            member.save()
            
            return Response(
                {
                    'message': 'Successfully joined club',
                    'club_id': club_id,
                    'club_name': club.name,
                    'member_count': club.member_count,
                },
                status=status.HTTP_200_OK
            )
        except Club.DoesNotExist:
            return Response(
                {'error': 'Club not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error joining club: {str(e)}")
            return Response(
                {'error': 'Failed to join club'},
                status=status.HTTP_400_BAD_REQUEST
            )


class LeaveClubView(generics.GenericAPIView):
    """Leave a club."""
    serializer_class = LeaveClubSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        club_id = serializer.validated_data['club_id']
        user_id = request.user.user_id
        
        try:
            # Get club
            club = Club.objects.get(club_id=club_id)
            
            # Check if owner - prevent owner from leaving
            if club.owner_id == user_id:
                return Response(
                    {'error': 'Club owner cannot leave the club'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Remove user from club
            if user_id in club.members:
                club.members.remove(user_id)
                club.member_count = max(0, club.member_count - 1)
                club.updated_at = timezone.now()
                club.save()
            
            # Remove club member record
            ClubMember.objects(
                club_id=club_id,
                user_id=user_id
            ).delete()
            
            return Response(
                {
                    'message': 'Successfully left club',
                    'club_id': club_id,
                    'club_name': club.name,
                },
                status=status.HTTP_200_OK
            )
        except Club.DoesNotExist:
            return Response(
                {'error': 'Club not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error leaving club: {str(e)}")
            return Response(
                {'error': 'Failed to leave club'},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserClubsView(generics.ListAPIView):
    """Get all clubs user is a member of."""
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        user_id = request.user.user_id
        
        try:
            # Get user's club memberships
            members = ClubMember.objects(user_id=user_id).order_by('-joined_at')
            
            clubs_data = []
            for member in members:
                try:
                    club = Club.objects.get(club_id=member.club_id)
                    club_data = {
                        'club_id': club.club_id,
                        'name': club.name,
                        'owner_username': club.owner_username,
                        'member_count': club.member_count,
                        'total_wins': club.total_wins,
                        'role': member.role,
                        'joined_at': member.joined_at,
                    }
                    clubs_data.append(club_data)
                except Club.DoesNotExist:
                    pass
            
            return Response({
                'count': len(clubs_data),
                'clubs': clubs_data,
            })
        except Exception as e:
            logger.error(f"Error retrieving user clubs: {str(e)}")
            return Response(
                {'error': 'Failed to retrieve clubs'},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserClubsDetailView(generics.GenericAPIView):
    """Get all clubs a user is a member of (by user_id)."""
    permission_classes = [AllowAny]
    
    def get(self, request, user_id, *args, **kwargs):
        try:
            # Get user's club memberships
            members = ClubMember.objects(user_id=user_id).order_by('-joined_at')
            
            clubs_data = []
            for member in members:
                try:
                    club = Club.objects.get(club_id=member.club_id)
                    club_data = {
                        'club_id': club.club_id,
                        'name': club.name,
                        'owner_username': club.owner_username,
                        'member_count': club.member_count,
                        'total_wins': club.total_wins,
                        'role': member.role,
                        'joined_at': member.joined_at,
                    }
                    clubs_data.append(club_data)
                except Club.DoesNotExist:
                    pass
            
            return Response({
                'count': len(clubs_data),
                'user_id': user_id,
                'clubs': clubs_data,
            })
        except Exception as e:
            logger.error(f"Error retrieving user clubs for {user_id}: {str(e)}")
            return Response(
                {'clubs': []},
                status=status.HTTP_200_OK
            )


class ClubStatsView(generics.GenericAPIView):
    """Get club statistics."""
    permission_classes = [AllowAny]
    
    def get(self, request, club_id, *args, **kwargs):
        try:
            club = Club.objects.get(club_id=club_id)
            serializer = ClubStatsSerializer(club)
            return Response(serializer.data)
        except Club.DoesNotExist:
            return Response(
                {'error': 'Club not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error retrieving club stats: {str(e)}")
            return Response(
                {'error': 'Failed to retrieve statistics'},
                status=status.HTTP_400_BAD_REQUEST
            )


class ClubMembersView(generics.ListAPIView):
    """Get all members of a club."""
    serializer_class = ClubMemberSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        club_id = self.kwargs.get('club_id')
        queryset = ClubMember.objects(club_id=club_id).order_by('-joined_at')
        return queryset
    
    def list(self, request, *args, **kwargs):
        club_id = self.kwargs.get('club_id')
        
        # Verify club exists
        try:
            Club.objects.get(club_id=club_id)
        except Club.DoesNotExist:
            return Response(
                {'error': 'Club not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': len(queryset),
            'members': serializer.data,
        })


class UpdateClubView(generics.GenericAPIView):
    """Update club information (owner only)."""
    serializer_class = UpdateClubSerializer
    permission_classes = [IsAuthenticated]
    
    def put(self, request, club_id, *args, **kwargs):
        try:
            club = Club.objects.get(club_id=club_id)
            
            # Check if user is club owner
            if club.owner_id != request.user.user_id:
                return Response(
                    {'error': 'Only club owner can update club information'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # Update fields
            if 'name' in serializer.validated_data:
                # Check if new name already exists
                existing = Club.objects(
                    name__iexact=serializer.validated_data['name']
                ).exclude('club_id', club.club_id)
                if existing:
                    return Response(
                        {'error': 'A club with this name already exists'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                club.name = serializer.validated_data['name']
            
            if 'description' in serializer.validated_data:
                club.description = serializer.validated_data['description']
            
            if 'logo_url' in serializer.validated_data:
                club.logo_url = serializer.validated_data['logo_url']
            
            club.updated_at = timezone.now()
            club.save()
            
            return Response(
                {
                    'message': 'Club updated successfully',
                    'club_id': club.club_id,
                },
                status=status.HTTP_200_OK
            )
        except Club.DoesNotExist:
            return Response(
                {'error': 'Club not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error updating club: {str(e)}")
            return Response(
                {'error': 'Failed to update club'},
                status=status.HTTP_400_BAD_REQUEST
            )
