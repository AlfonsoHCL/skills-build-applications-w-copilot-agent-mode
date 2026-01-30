from rest_framework import serializers
from .models import Team
from users.serializers import UserSerializer

class TeamSerializer(serializers.ModelSerializer):
    members_count = serializers.SerializerMethodField()
    leader_name = serializers.CharField(source='leader.get_full_name', read_only=True)
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'leader', 'leader_name', 'total_points', 'members_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_members_count(self, obj):
        return obj.members.count()

class TeamDetailSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    leader_name = serializers.CharField(source='leader.get_full_name', read_only=True)
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'leader', 'leader_name', 'members', 'total_points', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
