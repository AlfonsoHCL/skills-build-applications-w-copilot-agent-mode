from django.db import models
from users.models import User

class Achievement(models.Model):
    """Achievement/Badge model for gamification"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.ImageField(upload_to='achievements/')
    requirement_type = models.CharField(max_length=50)  # e.g., 'total_points', 'activities_count'
    requirement_value = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    """Through model for user achievements"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'achievement')
        ordering = ['-earned_at']
    
    def __str__(self):
        return f"{self.user} - {self.achievement.name}"
