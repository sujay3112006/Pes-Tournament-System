"""Users App Views"""
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import get_user_model
from apps.users.serializers import (
    CustomTokenObtainPairSerializer,
    UserRegistrationSerializer,
    UserDetailSerializer,
    UserUpdateSerializer,
    UserProfileSerializer,
    UserStatisticsSerializer,
    UserBadgeSerializer,
)
from apps.users.models import UserProfile, UserStatistics, UserBadge
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom token obtain view with user data."""
    serializer_class = CustomTokenObtainPairSerializer


class UserRegistrationView(generics.CreateAPIView):
    """User registration endpoint."""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create user profile in MongoDB
        try:
            UserProfile.objects.create(
                user_id=str(user.id),
                username=user.username,
                email=user.email,
                full_name=user.get_full_name(),
            )
            
            # Create initial statistics
            UserStatistics.objects.create(
                user_id=str(user.id),
            )
        except Exception as e:
            logger.error(f"Error creating user profile: {str(e)}")
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                'message': 'User registered successfully',
                'user': UserDetailSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class UserViewSet(viewsets.ModelViewSet):
    """User ViewSet for managing user accounts."""
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserDetailSerializer
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current user details."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        """Update user profile."""
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def profile(self, request, pk=None):
        """Get user profile details."""
        try:
            user = self.get_object()
            profile = UserProfile.objects.get(user_id=str(user.id))
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response(
                {'error': 'Profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Get user statistics."""
        try:
            user = self.get_object()
            stats = UserStatistics.objects.get(user_id=str(user.id))
            serializer = UserStatisticsSerializer(stats)
            return Response(serializer.data)
        except UserStatistics.DoesNotExist:
            return Response(
                {'error': 'Statistics not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['get'])
    def badges(self, request, pk=None):
        """Get user badges."""
        user = self.get_object()
        badges = UserBadge.objects.filter(user_id=str(user.id))
        serializer = UserBadgeSerializer(badges, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """Change user password."""
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not user.check_password(old_password):
            return Response(
                {'error': 'Invalid old password'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(new_password)
        user.save()
        
        return Response({'message': 'Password changed successfully'})
