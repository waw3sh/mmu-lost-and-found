"""
Create a new admin user with known credentials
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lostfound.settings')
django.setup()

from accounts.models import User
from django.contrib.auth.hashers import make_password

print("=" * 70)
print("CREATE NEW ADMIN USER")
print("=" * 70)

# Check if user already exists
existing_user = User.objects.filter(email='mmuadmin@lostfound.com').first()
if existing_user:
    print("User mmuadmin@lostfound.com already exists")
    print("Resetting password...")
    existing_user.password = make_password('Admin1234!')
    existing_user.save()
    print("Password reset successfully!")
else:
    print("Creating new admin user...")
    new_admin = User.objects.create(
        email='mmuadmin@lostfound.com',
        username='mmuadmin@lostfound.com',
        first_name='MMU',
        last_name='Administrator',
        password=make_password('Admin1234!'),
        role='ADMIN',
        is_staff=True,
        is_superuser=True,
        is_active=True,
        phone='+254700000000'
    )
    print("New admin user created successfully!")

print("\n" + "=" * 70)
print("NEW ADMIN CREDENTIALS:")
print("-" * 70)
print("Email: mmuadmin@lostfound.com")
print("Password: Admin1234!")
print("Role: ADMIN")
print("Status: Active")
print("=" * 70)

# Verify the user was created
verify_user = User.objects.filter(email='mmuadmin@lostfound.com').first()
if verify_user:
    print(f"\nVERIFICATION:")
    print(f"User exists: {verify_user.email}")
    print(f"Is admin: {verify_user.role}")
    print(f"Is staff: {verify_user.is_staff}")
    print(f"Is superuser: {verify_user.is_superuser}")
    print(f"Is active: {verify_user.is_active}")
else:
    print("\nERROR: User creation failed!")

print("\n" + "=" * 70)
print("DEPLOYMENT NEEDED:")
print("-" * 70)
print("1. This affects LOCAL database only")
print("2. Need to deploy to production")
print("3. Use production admin panel to create user")
print("4. Or access production database directly")
print("=" * 70)
