"""Users App URLs"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from apps.users.views import (
    CustomTokenObtainPairView,
    UserRegistrationView,
    UserViewSet,
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # JWT Token endpoints
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Registration
    path('register/', UserRegistrationView.as_view(), name='user_register'),
    
    # Users endpoints
    path('', include(router.urls)),
]
