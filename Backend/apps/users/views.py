"""Users App Views"""
from rest_framework import status, generics, viewsets, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.users.models import User, UserStatistics, UserBadge
from apps.users.serializers import (
    UserRegistrationSerializer,
    LoginSerializer,
    TokenResponseSerializer,
    UserProfileSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
    UserListSerializer,
)
from core.authentication import generate_token
from django.contrib.auth.hashers import make_password
import logging
import uuid
import base64

logger = logging.getLogger(__name__)


def generate_simple_token():
    """Generate a simple token for session management."""
    return base64.b64encode(str(uuid.uuid4()).encode()).decode()


class RegisterView(generics.CreateAPIView):
    """User registration endpoint."""
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            
            try:
                serializer.is_valid(raise_exception=True)
            except serializers.ValidationError as ve:
                logger.error(f"Registration validation error: {ve.detail}")
                errors = {}
                if isinstance(ve.detail, dict):
                    errors = {k: str(v[0]) if isinstance(v, list) else str(v) for k, v in ve.detail.items()}
                else:
                    errors = {'error': str(ve.detail)}
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            
            user = serializer.save()
            
            # Generate tokens using the new token store
            access_token = generate_token(user.user_id)
            refresh_token = generate_simple_token()
            
            logger.info(f"✅ New user {user.username} registered successfully")
            
            return Response(
                {
                    'message': 'User registered successfully',
                    'user': UserProfileSerializer(user).data,
                    'access': access_token,
                    'refresh': refresh_token,
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            logger.error(f"❌ Registration error (unexpected): {str(e)}", exc_info=True)
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class LoginView(generics.GenericAPIView):
    """User login endpoint."""
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            
            try:
                serializer.is_valid(raise_exception=True)
            except serializers.ValidationError as ve:
                logger.error(f"🔓 Login validation error: {ve.detail}")
                return Response(
                    {'error': str(ve.detail) if isinstance(ve.detail, str) else str(ve.detail[0]) if ve.detail else 'Validation failed'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user = serializer.validated_data['user']
            
            # Update last login
            from django.utils import timezone
            user.last_login = timezone.now()
            user.save()
            
            # Generate tokens using the new token store
            access_token = generate_token(user.user_id)
            refresh_token = generate_simple_token()
            
            logger.info(f"✅ User {user.username} logged in successfully. Access token: {access_token[:10]}...")
            
            return Response(
                {
                    'message': 'Login successful',
                    'user': UserProfileSerializer(user).data,
                    'access': access_token,
                    'refresh': refresh_token,
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"❌ Login error (unexpected): {str(e)}", exc_info=True)
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class ProfileView(generics.RetrieveUpdateAPIView):
    """Get or update current user profile."""
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return UserUpdateSerializer
        return UserProfileSerializer
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(
            {
                'message': 'Profile updated successfully',
                'user': UserProfileSerializer(instance).data,
            },
            status=status.HTTP_200_OK
        )


class ChangePasswordView(generics.GenericAPIView):
    """Change user password."""
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        user.password_hash = make_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response(
            {'message': 'Password changed successfully'},
            status=status.HTTP_200_OK
        )


class UserDetailView(generics.RetrieveAPIView):
    """Get user details by ID."""
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'user_id'
    lookup_url_kwarg = 'user_id'
    
    def get_queryset(self):
        return User.objects()
    
    def retrieve(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        try:
            user = User.objects.get(user_id=user_id)
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class UserStatisticsView(generics.RetrieveAPIView):
    """Get user statistics."""
    permission_classes = [IsAuthenticated]
    
    def retrieve(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        try:
            user = User.objects.get(user_id=user_id)
            stats = UserStatistics.objects.get(user_id=user_id)
            
            return Response({
                'user_id': user_id,
                'username': user.username,
                'total_tournaments': stats.total_tournaments,
                'total_matches': stats.total_matches,
                'match_wins': stats.match_wins,
                'match_losses': stats.match_losses,
                'match_draws': stats.match_draws,
                'win_rate': stats.win_rate,
                'goals_scored': stats.goals_scored,
                'goals_conceded': stats.goals_conceded,
                'clean_sheets': stats.clean_sheets,
                'points': stats.points,
                'ranking': stats.ranking,
            })
        except (User.DoesNotExist, UserStatistics.DoesNotExist):
            return Response(
                {'error': 'User or statistics not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class UserListView(generics.ListAPIView):
    """List all users with pagination and search."""
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = User.objects()
        
        # Search by username or email
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                username__icontains=search
            ) | User.objects(email__icontains=search)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class LogoutView(generics.GenericAPIView):
    """User logout endpoint (clear refresh token)."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refresh')
            logger.info(f"🚪 User {request.user.username} logging out...")
            
            # In a real app, you'd blacklist the token here
            # For now, just return success
            
            return Response(
                {'message': 'Logout successful'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"❌ Logout error: {str(e)}")
            return Response(
                {'error': 'Logout failed'},
                status=status.HTTP_400_BAD_REQUEST
            )
