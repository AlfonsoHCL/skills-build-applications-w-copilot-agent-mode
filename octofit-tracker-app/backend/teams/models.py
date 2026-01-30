from django.db import models
from users.models import User

class Team(models.Model):
    """Team model for group competitions"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='led_teams')
    members = models.ManyToManyField(User, related_name='teams')
    total_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-total_points', '-created_at']
    
    def __str__(self):
        return self.name
