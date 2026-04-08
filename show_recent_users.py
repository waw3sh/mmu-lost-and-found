"""
Show all registered users with their registration dates
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lostfound.settings')
django.setup()

from accounts.models import User
from django.utils import timezone
from datetime import timedelta

print("=" * 80)
print("MMU LOST & FOUND - REGISTERED USERS")
print("=" * 80)

# Get all users ordered by registration date (newest first)
users = User.objects.all().order_by('-date_joined')

print(f"Total Users: {users.count()}")
print("-" * 80)

print("RECENTLY REGISTERED USERS:")
print("-" * 80)

for i, user in enumerate(users, 1):
    # Calculate how long ago they registered
    time_diff = timezone.now() - user.date_joined
    days_ago = time_diff.days
    hours_ago = time_diff.seconds // 3600
    
    if days_ago == 0:
        time_ago = f"{hours_ago} hours ago"
    elif days_ago == 1:
        time_ago = "1 day ago"
    else:
        time_ago = f"{days_ago} days ago"
    
    print(f"{i:2d}. {user.first_name} {user.last_name}")
    print(f"    Email: {user.email}")
    print(f"    Phone: {user.phone or 'Not provided'}")
    print(f"    Role: {user.role}")
    print(f"    Student ID: {user.student_id or 'Not provided'}")
    print(f"    Registered: {user.date_joined.strftime('%Y-%m-%d %H:%M')} ({time_ago})")
    print(f"    Items: {user.reported_items.count()}")
    print("-" * 80)

print("\n" + "=" * 80)
print("USERS WITH PHONE NUMBERS (CAN RECEIVE SMS):")
print("-" * 80)

users_with_phone = User.objects.filter(phone__isnull=False).exclude(phone='').order_by('-date_joined')

for user in users_with_phone:
    print(f"• {user.first_name} {user.last_name} - {user.phone} ({user.email})")

print("\n" + "=" * 80)
print("ADMIN ACCESS:")
print("-" * 80)
print("URL: https://mmu-lost-and-found.onrender.com/admin/")
print("Admin: admin@mmu.ac.ke")
print("Password: Admin1234!")
print("=" * 80)
