"""Users App URLs"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from apps.users.views import (
    RegisterView,
    LoginView,
    ProfileView,
    ChangePasswordView,
    UserDetailView,
    UserStatisticsView,
    UserListView,
    LogoutView,
)

urlpatterns = [
    # Authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Profile
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/change-password/', ChangePasswordView.as_view(), name='change_password'),
    
    # Users
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<str:user_id>/', UserDetailView.as_view(), name='user_detail'),
    path('users/<str:user_id>/statistics/', UserStatisticsView.as_view(), name='user_statistics'),
]
