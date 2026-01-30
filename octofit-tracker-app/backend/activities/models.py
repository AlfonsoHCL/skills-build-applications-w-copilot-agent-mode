from django.db import models
from users.models import User

class Activity(models.Model):
    """Activity model for logging workouts"""
    ACTIVITY_TYPES = [
        ('running', 'Running'),
        ('walking', 'Walking'),
        ('strength', 'Strength Training'),
        ('cycling', 'Cycling'),
        ('swimming', 'Swimming'),
        ('sports', 'Sports'),
        ('yoga', 'Yoga'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    duration_minutes = models.IntegerField()  # Duration in minutes
    distance_km = models.FloatField(null=True, blank=True)  # Distance in kilometers
    calories_burned = models.IntegerField()
    points_earned = models.IntegerField(default=0)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user} - {self.activity_type} on {self.created_at.date()}"
