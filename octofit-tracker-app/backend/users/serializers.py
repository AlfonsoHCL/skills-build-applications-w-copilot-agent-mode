from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'points', 'bio', 'avatar', 'created_at']
        read_only_fields = ['id', 'created_at', 'points']

class UserDetailSerializer(serializers.ModelSerializer):
    activities_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'points', 'bio', 'avatar', 'activities_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_activities_count(self, obj):
        return obj.activities.count()

class UserLeaderboardSerializer(serializers.ModelSerializer):
    rank = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'points', 'rank']
    
    def get_rank(self, obj):
        # This will be calculated in the view
        return None
