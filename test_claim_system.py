"""
Test OTP claim system
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lostfound.settings')
django.setup()

from items.models import Item
from accounts.models import User
from claims.models import Claim

print("=" * 70)
print("TESTING OTP CLAIM SYSTEM")
print("=" * 70)

# Find items in "found" status
found_items = Item.objects.filter(status='found')
print(f"Found {found_items.count()} items with status 'found':")
print("-" * 50)

for item in found_items:
    print(f"Item: {item.name}")
    print(f"ID: {item.id}")
    print(f"UUID: {item.uuid}")
    print(f"Status: {item.status}")
    print(f"Reporter: {item.reporter.email if item.reporter else 'None'}")
    print("-" * 50)

# Find users who can test claims
test_users = User.objects.filter(phone__isnull=False).exclude(phone='').order_by('-date_joined')[:3]
print(f"\nTest users with phone numbers:")
print("-" * 50)

for user in test_users:
    print(f"User: {user.first_name} {user.last_name}")
    print(f"Email: {user.email}")
    print(f"Phone: {user.phone}")
    print(f"Role: {user.role}")
    print("-" * 50)

print("\n" + "=" * 70)
print("CLAIM TEST LINKS:")
print("-" * 50)

# Generate claim links for found items
for item in found_items[:3]:  # Show first 3 items
    claim_url = f"https://mmu-lost-and-found.onrender.com/claims/create/{item.id}/"
    print(f"Item: {item.name}")
    print(f"Claim URL: {claim_url}")
    print("-" * 50)

print("\n" + "=" * 70)
print("OTP CLAIM PROCESS:")
print("-" * 50)
print("1. User logs in")
print("2. User navigates to claim URL")
print("3. User enters 6-digit OTP code")
print("4. User selects handoff method")
print("5. User submits claim")
print("6. Claim is created with OTP verification")
print("=" * 70)
