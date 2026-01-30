from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from .models import User
from .serializers import UserSerializer, UserDetailSerializer, UserLeaderboardSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'username']
    ordering_fields = ['points', 'created_at']
    ordering = ['-points']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action == 'leaderboard':
            return UserLeaderboardSerializer
        return UserSerializer
    
    @action(detail=False, methods=['get'])
    def leaderboard(self, request):
        """Get user leaderboard ranked by points"""
        users = User.objects.filter(role='student').order_by('-points')
        serializer = self.get_serializer(users, many=True)
        
        # Add rank to each user
        data = []
        for idx, item in enumerate(serializer.data, start=1):
            item['rank'] = idx
            data.append(item)
        
        return Response(data)
    
    @action(detail=True, methods=['get'])
    def activities(self, request, pk=None):
        """Get all activities for a specific user"""
        user = self.get_object()
        activities = user.activities.all()
        from activities.serializers import ActivitySerializer
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def achievements(self, request, pk=None):
        """Get all achievements for a specific user"""
        user = self.get_object()
        achievements = user.achievements.all()
        from achievements.serializers import UserAchievementSerializer
        serializer = UserAchievementSerializer(achievements, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user details"""
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)
