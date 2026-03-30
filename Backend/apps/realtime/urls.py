"""Realtime App URLs"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.realtime.views import NotificationViewSet

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
]
