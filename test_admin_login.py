"""
Test admin login redirection
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lostfound.settings')
django.setup()

from accounts.models import User

print("=" * 70)
print("TESTING ADMIN LOGIN REDIRECTION")
print("=" * 70)

# Find admin users
admin_users = User.objects.filter(role='ADMIN')
print(f"Found {admin_users.count()} admin users:")
print("-" * 50)

for admin in admin_users:
    print(f"Email: {admin.email}")
    print(f"Name: {admin.first_name} {admin.last_name}")
    print(f"Role: {admin.role}")
    print(f"Is Staff: {admin.is_staff}")
    print(f"Is Superuser: {admin.is_superuser}")
    print(f"Is Active: {admin.is_active}")
    print("-" * 50)

print("\n" + "=" * 70)
print("LOGIN REDIRECTION LOGIC:")
print("-" * 50)
print("1. User logs in with email/password")
print("2. System checks if user.role == 'ADMIN'")
print("3. If ADMIN: redirect to /accounts/admin-dashboard/")
print("4. If NOT ADMIN: redirect to /dashboard/")
print("5. Admin dashboard shows admin privileges")
print("6. Regular dashboard shows user data")
print("=" * 70)

print("\n" + "=" * 70)
print("EXPECTED BEHAVIOR:")
print("-" * 50)
print("Admin login should redirect to:")
print("https://mmu-lost-and-found.onrender.com/accounts/admin-dashboard/")
print("\nRegular user login should redirect to:")
print("https://mmu-lost-and-found.onrender.com/dashboard/")
print("\nAdmin users will also see 'Admin Dashboard' link in regular dashboard")
print("=" * 70)

print("\n" + "=" * 70)
print("TESTING CREDENTIALS:")
print("-" * 50)
print("Try these admin credentials:")
print("Email: admin@mmu.ac.ke")
print("Password: Admin1234!")
print("\nAlternative:")
print("Email: mmuadmin@lostfound.com")
print("Password: Admin1234!")
print("=" * 70)
