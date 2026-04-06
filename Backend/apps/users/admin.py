"""Users App Admin"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Mongoengine models don't work with Django admin
# @admin.register(User)
# class UserAdmin(BaseUserAdmin):
#     """User admin configuration."""
#     list_display = ('id', 'username', 'email', 'is_verified', 'is_premium', 'date_joined')
#     list_filter = ('is_verified', 'is_premium', 'is_staff', 'is_active')
#     search_fields = ('username', 'email', 'first_name', 'last_name')
#     readonly_fields = ('date_joined', 'last_login', 'user_id')
#     
#     fieldsets = BaseUserAdmin.fieldsets + (
#         ('Additional Info', {'fields': ('user_id', 'bio', 'avatar', 'phone_number', 'birth_date')}),
#         ('Verification', {'fields': ('is_verified', 'is_premium')}),
#     )
