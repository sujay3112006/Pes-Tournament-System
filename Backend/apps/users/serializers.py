"""Users App Serializers"""
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import User, UserStatistics, UserBadge
from django.contrib.auth.hashers import make_password
from django.utils import timezone
import re


class UserRegistrationSerializer(serializers.Serializer):
    """Serializer for user registration."""
    username = serializers.CharField(min_length=3, max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)
    password_confirm = serializers.CharField(min_length=8, write_only=True)
    first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    
    def validate_username(self, value):
        """Validate username format and uniqueness."""
        if not re.match(r'^[a-zA-Z0-9_-]+$', value):
            raise serializers.ValidationError(
                "Username can only contain letters, numbers, underscores, and hyphens."
            )
        if User.objects(username=value).first():
            raise serializers.ValidationError("Username already exists.")
        return value
    
    def validate_email(self, value):
        """Validate email uniqueness."""
        if User.objects(email=value).first():
            raise serializers.ValidationError("Email already registered.")
        return value.lower()
    
    def validate_password(self, value):
        """Validate password strength."""
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter."
            )
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError(
                "Password must contain at least one lowercase letter."
            )
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError(
                "Password must contain at least one digit."
            )
        return value
    
    def validate(self, data):
        """Validate password confirmation."""
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({
                'password': 'Passwords do not match.'
            })
        return data
    
    def create(self, validated_data):
        """Create user with hashed password."""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        # Create user with hashed password
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            password_hash=make_password(password),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            is_active=True,
        )
        user.save()
        
        # Create user statistics
        try:
            UserStatistics.objects.create(user_id=user.user_id)
        except Exception:
            pass
        
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        """Validate username and password."""
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            raise serializers.ValidationError(
                "Username and password are required."
            )
        
        # Find user by username
        user = User.objects(username=username).first()
        
        if not user:
            raise serializers.ValidationError(
                "Invalid username or password."
            )
        
        if not user.is_active:
            raise serializers.ValidationError(
                "User account is inactive."
            )
        
        # Check password (assuming password_hash is stored)
        from django.contrib.auth.hashers import check_password
        if not check_password(password, user.password_hash):
            raise serializers.ValidationError(
                "Invalid username or password."
            )
        
        data['user'] = user
        return data


class TokenResponseSerializer(serializers.Serializer):
    """Serializer for token response."""
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        user = obj.get('user')
        if user:
            return UserProfileSerializer(user).data
        return None


class UserProfileSerializer(serializers.Serializer):
    """Serializer for user profile."""
    user_id = serializers.CharField(read_only=True)
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    bio = serializers.CharField(required=False, allow_blank=True)
    avatar_url = serializers.URLField(required=False, allow_blank=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    country = serializers.CharField(required=False, allow_blank=True)
    coins = serializers.IntegerField(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)
    is_premium = serializers.BooleanField(read_only=True)
    stats = serializers.JSONField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class UserUpdateSerializer(serializers.Serializer):
    """Serializer for updating user profile."""
    first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    bio = serializers.CharField(max_length=500, required=False, allow_blank=True)
    avatar_url = serializers.URLField(required=False, allow_blank=True)
    phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True)
    country = serializers.CharField(max_length=100, required=False, allow_blank=True)
    
    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.updated_at = timezone.now()
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing password."""
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(min_length=8, write_only=True)
    new_password_confirm = serializers.CharField(min_length=8, write_only=True)
    
    def validate_old_password(self, value):
        """Validate old password."""
        user = self.context.get('request').user
        from django.contrib.auth.hashers import check_password
        if not check_password(value, user.password_hash):
            raise serializers.ValidationError("Old password is incorrect.")
        return value
    
    def validate_new_password(self, value):
        """Validate new password strength."""
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter."
            )
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError(
                "Password must contain at least one lowercase letter."
            )
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError(
                "Password must contain at least one digit."
            )
        return value
    
    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError({
                'new_password': 'Passwords do not match.'
            })
        return data


class UserListSerializer(serializers.Serializer):
    """Serializer for listing users."""
    user_id = serializers.CharField(read_only=True)
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    coins = serializers.IntegerField(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
