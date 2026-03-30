"""Users App Serializers"""
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from apps.users.models import UserProfile, UserStatistics, UserBadge

User = get_user_model()


class UserProfileSerializer(serializers.Serializer):
    """Serializer for user profile."""
    user_id = serializers.CharField(read_only=True)
    username = serializers.CharField()
    email = serializers.EmailField()
    full_name = serializers.CharField()
    bio = serializers.CharField(required=False)
    avatar_url = serializers.URLField(required=False)
    phone_number = serializers.CharField(required=False)
    country = serializers.CharField(required=False)
    is_verified = serializers.BooleanField(read_only=True)
    is_premium = serializers.BooleanField()
    rating = serializers.CharField(read_only=True)
    total_tournaments = serializers.IntegerField(read_only=True)
    total_matches_played = serializers.IntegerField(read_only=True)
    win_rate = serializers.FloatField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class UserStatisticsSerializer(serializers.Serializer):
    """Serializer for user statistics."""
    user_id = serializers.CharField(read_only=True)
    total_points = serializers.IntegerField()
    total_badges = serializers.IntegerField()
    tournament_wins = serializers.IntegerField()
    match_wins = serializers.IntegerField()
    match_losses = serializers.IntegerField()
    match_draws = serializers.IntegerField()
    goal_scored = serializers.IntegerField()
    goal_conceded = serializers.IntegerField()
    clean_sheets = serializers.IntegerField()


class UserBadgeSerializer(serializers.Serializer):
    """Serializer for user badges."""
    user_id = serializers.CharField(read_only=True)
    badge_name = serializers.CharField()
    badge_icon = serializers.URLField()
    earned_at = serializers.DateTimeField(read_only=True)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT token serializer with user data."""
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['full_name'] = user.get_full_name()
        
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add user data to response
        user = self.user
        data['user'] = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'full_name': user.get_full_name(),
        }
        
        return data


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm', 'first_name', 'last_name')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer for user details."""
    profile = UserProfileSerializer(read_only=True)
    statistics = UserStatisticsSerializer(read_only=True)
    badges = UserBadgeSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'profile', 'statistics', 'badges')


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user details."""
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
