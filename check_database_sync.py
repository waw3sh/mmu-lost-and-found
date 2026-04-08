"""
Check if local database matches live site database
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lostfound.settings')
django.setup()

from accounts.models import User

print("=" * 80)
print("DATABASE SYNC CHECK - LOCAL vs PRODUCTION")
print("=" * 80)

# Check local database
print("LOCAL DATABASE USERS:")
print("-" * 80)

local_users = User.objects.all().order_by('-date_joined')
print(f"Total Users (Local): {local_users.count()}")

# Look for the specific user you mentioned
tess_user = User.objects.filter(email='tess@gmail.com').first()

if tess_user:
    print(f"FOUND tess@gmail.com in local database:")
    print(f"   Name: {tess_user.first_name} {tess_user.last_name}")
    print(f"   Phone: {tess_user.phone}")
    print(f"   Role: {tess_user.role}")
    print(f"   Registered: {tess_user.date_joined}")
    print(f"   Items: {tess_user.reported_items.count()}")
else:
    print("tess@gmail.com NOT FOUND in local database")

print("\n" + "=" * 80)
print("RECENT LOCAL REGISTRATIONS:")
print("-" * 80)

for user in local_users[:10]:
    print(f"• {user.email} - {user.first_name} {user.last_name} - {user.date_joined.strftime('%Y-%m-%d %H:%M')}")

print("\n" + "=" * 80)
print("POSSIBLE ISSUES:")
print("-" * 80)
print("1. Local database is different from production database")
print("2. Render.com uses PostgreSQL, local might use SQLite")
print("3. Live site registrations go to production database")
print("4. Local script checks local database only")
print("\n" + "=" * 80)
print("SOLUTIONS:")
print("-" * 80)
print("1. Check admin panel on live site for tess@gmail.com")
print("2. Use production debug endpoint to check users")
print("3. Ensure database migrations are applied on production")
print("4. Check if user registration is working on production")
print("=" * 80)
