"""
Check production vs local database users
Run this to see the difference between databases
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lostfound.settings')
django.setup()

from accounts.models import User

print("=" * 60)
print("DATABASE COMPARISON TOOL")
print("=" * 60)

# Get all users from current database
users = User.objects.all()
print(f"Current database users: {users.count()}")
print()

print("All registered users:")
for i, user in enumerate(users.order_by('-date_joined'), 1):
    print(f"{i:2d}. {user.email}")
    print(f"    Name: {user.first_name} {user.last_name}")
    print(f"    Role: {user.role}")
    print(f"    Registered: {user.date_joined.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"    Phone: {user.phone}")
    print()

print("=" * 60)
print("INSTRUCTIONS:")
print("1. If you're checking LOCAL development:")
print("   - Run this script locally")
print("   - Compare with production admin")
print()
print("2. To see PRODUCTION users:")
print("   - Go to: https://mmu-lost-and-found.onrender.com/admin/")
print("   - Login: admin@mmu.ac.ke / Admin1234!")
print("   - Check Users section")
print()
print("3. To sync users:")
print("   - Users register on PRODUCTION appear there immediately")
print("   - Local database is separate for development")
print("=" * 60)
