from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Activity
from .serializers import ActivitySerializer, ActivityDetailSerializer

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['activity_type', 'user__first_name', 'user__last_name']
    ordering_fields = ['created_at', 'points_earned', 'duration_minutes']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ActivityDetailSerializer
        return ActivitySerializer
    
    def get_queryset(self):
        """Filter activities by current user unless they are a teacher"""
        user = self.request.user
        if user.role == 'teacher':
            return Activity.objects.all()
        return Activity.objects.filter(user=user)
    
    def perform_create(self, serializer):
        """Create activity for current user"""
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent activities"""
        activities = self.get_queryset()[:10]
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get activities grouped by type with count"""
        activities = self.get_queryset()
        from django.db.models import Count
        activity_counts = Activity.objects.values('activity_type').annotate(count=Count('id'))
        return Response(activity_counts)
