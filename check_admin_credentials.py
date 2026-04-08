"""
Check admin login credentials in the database
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lostfound.settings')
django.setup()

from accounts.models import User

print("=" * 70)
print("ADMIN CREDENTIALS CHECK")
print("=" * 70)

# Find all admin users
admin_users = User.objects.filter(role='ADMIN')
print(f"Found {admin_users.count()} admin users:")
print("-" * 70)

for admin in admin_users:
    print(f"Email: {admin.email}")
    print(f"Name: {admin.first_name} {admin.last_name}")
    print(f"Role: {admin.role}")
    print(f"Phone: {admin.phone}")
    print(f"Is Staff: {admin.is_staff}")
    print(f"Is Superuser: {admin.is_superuser}")
    print(f"Date Joined: {admin.date_joined}")
    print("-" * 70)

# Also check for any superusers
superusers = User.objects.filter(is_superuser=True)
if superusers.exists():
    print(f"\nFound {superusers.count()} superusers:")
    print("-" * 70)
    for su in superusers:
        print(f"Email: {su.email}")
        print(f"Name: {su.first_name} {su.last_name}")
        print(f"Is Staff: {su.is_staff}")
        print(f"Is Superuser: {su.is_superuser}")
        print("-" * 70)

# Check specific email we were using
specific_admin = User.objects.filter(email='admin@mmu.ac.ke').first()
if specific_admin:
    print(f"\nChecking specific admin@mmu.ac.ke:")
    print("-" * 70)
    print(f"Email: {specific_admin.email}")
    print(f"Name: {specific_admin.first_name} {specific_admin.last_name}")
    print(f"Role: {specific_admin.role}")
    print(f"Is Staff: {specific_admin.is_staff}")
    print(f"Is Superuser: {specific_admin.is_superuser}")
    print(f"Is Active: {specific_admin.is_active}")
else:
    print(f"\nadmin@mmu.ac.ke NOT FOUND in database")

print("\n" + "=" * 70)
print("RECOMMENDED LOGIN CREDENTIALS:")
print("-" * 70)

# Find the first admin user for login
first_admin = User.objects.filter(role='ADMIN').first()
if first_admin:
    print(f"Email: {first_admin.email}")
    print(f"Password: [You know the password]")
    print(f"Role: {first_admin.role}")
else:
    print("No admin users found!")

print("=" * 70)
