import os
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'octofit_project.settings')
django.setup()

from users.models import User
from activities.models import Activity
from teams.models import Team
from achievements.models import Achievement, UserAchievement

def clear_database():
    """Clear existing data"""
    User.objects.all().delete()
    Activity.objects.all().delete()
    Team.objects.all().delete()
    Achievement.objects.all().delete()
    UserAchievement.objects.all().delete()
    print("✓ Database cleared")

def create_users():
    """Create sample users"""
    users = []
    teacher = User.objects.create_user(
        username='paul_octo',
        email='paul@mergington.edu',
        first_name='Paul',
        last_name='Octo',
        role='teacher',
        points=500
    )
    users.append(teacher)
    
    # Create student users
    student_names = [
        ('Alex', 'Johnson'),
        ('Bailey', 'Smith'),
        ('Casey', 'Williams'),
        ('Dana', 'Brown'),
        ('Evan', 'Davis'),
        ('Fiona', 'Miller'),
        ('Gabe', 'Wilson'),
        ('Hannah', 'Moore'),
        ('Isaac', 'Taylor'),
        ('Julia', 'Anderson'),
    ]
    
    for first_name, last_name in student_names:
        user = User.objects.create_user(
            username=f"{first_name.lower()}_{last_name.lower()}",
            email=f"{first_name.lower()}@mergington.edu",
            first_name=first_name,
            last_name=last_name,
            role='student',
            points=random.randint(50, 400)
        )
        users.append(user)
    
    print(f"✓ Created {len(users)} users")
    return users

def create_activities(users):
    """Create sample activities"""
    activity_types = ['running', 'walking', 'strength', 'cycling', 'swimming', 'sports', 'yoga']
    activities = []
    
    for user in users[1:]:  # Skip teacher
        num_activities = random.randint(3, 8)
        for _ in range(num_activities):
            activity_type = random.choice(activity_types)
            activity = Activity.objects.create(
                user=user,
                activity_type=activity_type,
                duration_minutes=random.randint(15, 120),
                distance_km=random.uniform(1.0, 15.0) if random.choice([True, False]) else None,
                calories_burned=random.randint(100, 800),
                points_earned=random.randint(10, 100),
                notes=f"Great {activity_type} session!" if random.choice([True, False]) else None,
                created_at=datetime.now() - timedelta(days=random.randint(0, 30))
            )
            activities.append(activity)
    
    print(f"✓ Created {len(activities)} activities")
    return activities

def create_teams(users):
    """Create sample teams"""
    teacher = users[0]
    teams = []
    
    team_names = ['Team Alpha', 'Team Beta', 'Team Gamma', 'Team Delta']
    
    for i, team_name in enumerate(team_names):
        team = Team.objects.create(
            name=team_name,
            description=f"This is {team_name} for the fitness challenge",
            leader=teacher,
            total_points=random.randint(500, 2000)
        )
        # Add random members to team
        members = random.sample(users[1:], k=random.randint(2, 4))
        team.members.set(members)
        teams.append(team)
    
    print(f"✓ Created {len(teams)} teams")
    return teams

def create_achievements():
    """Create sample achievements"""
    achievements = [
        {
            'name': 'First Step',
            'description': 'Complete your first activity',
            'requirement_type': 'activities_count',
            'requirement_value': 1,
        },
        {
            'name': 'Getting Started',
            'description': 'Log 10 activities',
            'requirement_type': 'activities_count',
            'requirement_value': 10,
        },
        {
            'name': 'Fitness Enthusiast',
            'description': 'Earn 500 points',
            'requirement_type': 'total_points',
            'requirement_value': 500,
        },
        {
            'name': 'Champion',
            'description': 'Earn 1000 points',
            'requirement_type': 'total_points',
            'requirement_value': 1000,
        },
        {
            'name': 'Marathon Runner',
            'description': 'Complete a 30+ minute activity',
            'requirement_type': 'long_activity',
            'requirement_value': 30,
        },
    ]
    
    created_achievements = []
    for ach_data in achievements:
        achievement = Achievement.objects.create(
            name=ach_data['name'],
            description=ach_data['description'],
            requirement_type=ach_data['requirement_type'],
            requirement_value=ach_data['requirement_value']
        )
        created_achievements.append(achievement)
    
    print(f"✓ Created {len(created_achievements)} achievements")
    return created_achievements

def assign_achievements(users, achievements):
    """Assign achievements to users"""
    assignments = 0
    for user in users:
        if user.points >= 500:
            UserAchievement.objects.get_or_create(
                user=user,
                achievement=achievements[2]  # Fitness Enthusiast
            )
            assignments += 1
        
        if user.points >= 1000:
            UserAchievement.objects.get_or_create(
                user=user,
                achievement=achievements[3]  # Champion
            )
            assignments += 1
        
        if user.activities.count() >= 1:
            UserAchievement.objects.get_or_create(
                user=user,
                achievement=achievements[0]  # First Step
            )
            assignments += 1
    
    print(f"✓ Assigned {assignments} achievement instances")

def main():
    """Run all seeding functions"""
    print("🌱 Starting OctoFit database population...")
    print()
    
    clear_database()
    users = create_users()
    create_activities(users)
    create_teams(users)
    achievements = create_achievements()
    assign_achievements(users, achievements)
    
    print()
    print("✅ OctoFit database population complete!")

if __name__ == '__main__':
    main()
