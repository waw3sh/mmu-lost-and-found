"""
Reset admin password to a known value
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lostfound.settings')
django.setup()

from accounts.models import User
from django.contrib.auth.hashers import make_password

print("=" * 70)
print("RESET ADMIN PASSWORD")
print("=" * 70)

# Find admin users
admin_users = User.objects.filter(role='ADMIN')

for admin in admin_users:
    print(f"Admin found: {admin.email}")
    
    # Reset password to a known value
    new_password = "Admin1234!"
    admin.password = make_password(new_password)
    admin.save()
    
    print(f"Password reset for {admin.email}")
    print(f"New password: {new_password}")
    print("-" * 70)

print("\n" + "=" * 70)
print("LOGIN CREDENTIALS AFTER RESET:")
print("-" * 70)

first_admin = User.objects.filter(role='ADMIN').first()
if first_admin:
    print(f"Email: {first_admin.email}")
    print(f"Password: Admin1234!")
    print(f"Role: {first_admin.role}")

print("\n" + "=" * 70)
print("PRODUCTION DEPLOYMENT NEEDED:")
print("-" * 70)
print("1. This reset affects LOCAL database only")
print("2. Production database may have different password")
print("3. Deploy this reset to production if needed")
print("4. Or use production admin panel to reset")
print("=" * 70)
